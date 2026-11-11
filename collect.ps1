param(
    [Parameter(Mandatory)]
    [string[]]$Servers,
    [Parameter(Mandatory)]
    [string[]]$Rooms,
)

$DomainControllers = @()
foreach ($dc in $Servers) {
    $obj = New-Object System.DirectoryServices.DirectoryEntry("LDAP://$dc")
    $DomainControllers += $obj
}

$searcher = New-Object System.DirectoryServices.DirectorySearcher
$searcher.Filter = $Filter
$searcher.SearchRoot = $DomainControllers[0]

$now = ([DateTimeOffset][datetime]::Now).ToUnixTimeSeconds()

$resultset = @()
foreach ($room in $rooms) {
	$times = @{}
	foreach ($obj in $DomainControllers) {
	    $searcher.SearchRoot = $obj
	    # TODO: Maybe a system that lets me specify a format string as a parameter
	    $searcher.Filter = "(&(objectClass=computer)(name=*-LAB-$room))"
	    
	    foreach ($res in $searcher.FindAll()) {
	        $name = $res.Properties.name[0]
	        $lastlogon = $res.Properties.lastlogon[0]
	        # stackoverflow.com/a/34271940
	        $lastlogondt = [datetime]::FromFileTime($lastlogon)
	        $lastlogondt = ([DateTimeOffset]$lastlogondt).ToUnixTimeSeconds()
	        if ($times.Contains($name)) {
	            if ($lastlogondt -gt $times[$name]) {
	                $times[$name] = $lastlogondt
	            }
	        } else {
	            $times[$name] = $lastlogondt
	        }
	    }
	}
	$resultset += @{
		name = "Room $room"
		times = $times
	}
}

ConvertTo-JSON -Depth 3 -InputObject @{
    rooms = $results
    collected_at = $now
}
