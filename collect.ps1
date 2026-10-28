param(
    [Parameter(Mandatory)]
    [string[]]$Servers,
    [Parameter(Mandatory)]
    [string]$Filter
)

$DomainControllers = @()
foreach ($dc in $Servers) {
    $obj = New-Object System.DirectoryServices.DirectoryEntry("LDAP://$dc")
    $DomainControllers += $obj
}

$searcher = New-Object System.DirectoryServices.DirectorySearcher
$searcher.Filter = $Filter
$searcher.SearchRoot = $DomainControllers[0]

$results = @{}

foreach ($obj in $DomainControllers) {
    $searcher.SearchRoot = $obj
    
    foreach ($res in $searcher.FindAll()) {
        $name = $res.Properties.name[0]
        $lastlogon = $res.Properties.lastlogon[0]
        # stackoverflow.com/a/34271940
        $lastlogondt = [datetime]::FromFileTime($lastlogon)
        $lastlogondt = ([DateTimeOffset]$lastlogondt).ToUnixTimeSeconds()
        if ($results.Contains($name)) {
            if ($lastlogondt -gt $results[$name]) {
                $results[$name] = $lastlogondt
            }
        } else {
            $results[$name] = $lastlogondt
        }
    }
}

ConvertTo-JSON -InputObject $results