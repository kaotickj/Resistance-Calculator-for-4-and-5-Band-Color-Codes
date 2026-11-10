#define AppVersion "3.0.0"
[Setup]
AppId={{45837032-D36C-42E7-82D3-0B57E108F624}
AppName=Resistor Color Code Calculator
AppVersion={#AppVersion}
AppPublisher=KaotickJ
AppPublisherURL=https://github.com/kaotickj
DefaultDirName={localappdata}\Programs\ResistorCalculator
DefaultGroupName=Resistor Color Code Calculator
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir=..\..\dist
OutputBaseFilename=ResistorCalculator-{#AppVersion}-windows-x86_64-setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
LicenseFile=..\..\stage\LICENSE
InfoBeforeFile=..\..\stage\README.txt
UninstallDisplayIcon={app}\icon.ico
[Files]
Source: "..\..\stage\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{group}\Resistor Color Code Calculator"; Filename: "{app}\runtime\.venv\Scripts\pythonw.exe"; Parameters: """{app}\runtime\resistanceCalculator.py"""; WorkingDir: "{app}\runtime"; IconFilename: "{app}\icon.ico"
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"
[UninstallDelete]
Type: filesandordirs; Name: "{app}\runtime"
Type: files; Name: "{app}\resistor-calculator-install.log"
[Code]
function PrepareToInstall(var NeedsRestart: Boolean): String;
var Code: Integer;
begin
  Result := '';
  if not Exec('py.exe', '-3.12 -c "import struct; assert struct.calcsize(''P'') == 8"', '', SW_HIDE, ewWaitUntilTerminated, Code) then
    Result := 'Install 64-bit Python 3.12 with the Python launcher from python.org, then run this installer again.'
  else if Code <> 0 then
    Result := '64-bit Python 3.12 is required. Install it from python.org, then run this installer again.';
  if DirExists(ExpandConstant('{app}\runtime')) then
    Result := 'This version is already installed. Uninstall it before reinstalling.';
end;
procedure CurStepChanged(CurStep: TSetupStep);
var Code: Integer;
begin
  if CurStep = ssPostInstall then begin
    if not Exec('py.exe', '-3.12 "' + ExpandConstant('{app}\install.py') + '" --target "' + ExpandConstant('{app}\runtime') + '" --no-shortcut', ExpandConstant('{app}'), SW_HIDE, ewWaitUntilTerminated, Code) then
      RaiseException('Could not launch Python. Installation is incomplete.');
    if Code <> 0 then
      RaiseException('Dependency installation failed. See resistor-calculator-install.log in the installation folder. Uninstall and retry after fixing Python/network access.');
  end;
end;
