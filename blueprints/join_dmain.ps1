# Join VM to domain
# ------------------------------

# parameters
$DOMAIN_NAME = "dc1.lab"
$DC_USER = "svc"
$DC_PASSWORD = "nx2Tech911!"

function Set-Hostname{
    [CmdletBinding()]
    Param(
        [parameter(Mandatory=$true)]
        [string]$Hostname
  )
    if ($Hostname -eq  $(hostname)){
      Write-Host "Hostname already set."
    }
    else{
      Rename-Computer -NewName $HOSTNAME -ErrorAction Stop
    }
  }
  
  function JointoDomain {
    [CmdletBinding()]
    Param(
        [parameter(Mandatory=$true)]
        [string]$DomainName,
        [parameter(Mandatory=$false)]
        [string]$OU,
        [parameter(Mandatory=$true)]
        [string]$Username,
        [parameter(Mandatory=$true)]
        [string]$Password
    )
  
    if ($env:computername  -eq $env:userdomain) {
      Write-Host "Not in domain"
      $adminname = "$DomainName\$Username"
      $adminpassword = ConvertTo-SecureString -asPlainText -Force -String "$Password"
      Write-Host "$adminname , $password"
      $credential = New-Object System.Management.Automation.PSCredential($adminname,$adminpassword)
      Add-computer -DomainName $DomainName -Credential $credential -force -Options JoinWithNewName,AccountCreate -PassThru -ErrorAction Stop
    }
    else {
       Write-Host "Already in domain"
    }
  }

  JointoDomain -DomainName $DOMAIN_NAME -Username $DC_USER -Password $DC_PASSWORD