$searcher = New-Object System.DirectoryServices.DirectorySearcher
$dc01 = New-Object System.DirectoryServices.DirectoryEntry("LDAP://[ censored ]")
$dc02 = New-Object System.DirectoryServices.DirectoryEntry("LDAP://[ censored ]")

$searcher.Filter = "(&(objectClass=computer)(name=[ censored ]-*))"
$searcher.SearchRoot = $dc01

$results = @{}
foreach ($res in $searcher.FindAll()) {
    $name = $res.Properties.name[0]
    $lastlogon = $res.Properties.lastlogon[0]
    # stackoverflow.com/a/34271940
    $lastlogondt = [datetime]::FromFileTime($lastlogon)
    $lastlogondt = ([DateTimeOffset]$lastlogondt).ToUnixTimeSeconds()
    $results.Add($name, $lastlogondt)
}

$searcher.SearchRoot = $dc02

foreach ($res in $searcher.FindAll()) {
    $name = $res.Properties.name[0]
    $lastlogon = $res.Properties.lastlogon[0]
    $lastlogondt = [datetime]::FromFileTime($lastlogon)
    $lastlogondt = ([DateTimeOffset]$lastlogondt).ToUnixTimeSeconds()
    if ($lastlogondt -gt $results[$name]) {
        $results[$name] = $lastlogondt
    }
}

ConvertTo-JSON -InputObject $results