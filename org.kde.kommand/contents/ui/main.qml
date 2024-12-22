// plasmoidviewer --applet org.kde.kommand
// kpackagetool5 -t Plasma/Applet --install org.kde.kommand
// kpackagetool5 -t Plasma/Applet --upgrade org.kde.kommand
// kpackagetool5 -t Plasma/Applet --remove org.kde.kommand
// https://doc.qt.io/qt-6/qtquick-controls-qmlmodule.html
// https://develop.kde.org/docs/getting-started/kirigami/
import QtQuick 2.0
import org.kde.plasma.plasmoid 2.0
import org.kde.plasma.core 2.0 as PlasmaCore
import QtQuick.Layouts 1.1

Item {
	id: main
	width: units.gridUnit * 2;
	height: units.gridUnit * 2;
	property bool status: false
	property string mic_on: "audio-recorder-on"
	property string mic_off: "audio-recorder-off"
	property string localPath: plasmoid.configuration.localPath
	property string command: "python3 "+localPath+"/contents/code/main.py "+plasmoid.configuration.language
	Plasmoid.icon: status ? mic_on : mic_off
	Plasmoid.status: {
		if(status){
			return PlasmaCore.Types.ActiveStatus;
		}
		return PlasmaCore.Types.PassiveStatus;
	}
	Plasmoid.onActivated: toggle()
	function toggle() {
		if(status){
			status = false;
		}else{
			status = true;
		}
	}
	PlasmaCore.IconItem {
		id: defaultIcon
		anchors.fill: parent
		source: status ? mic_on : mic_off
		visible: true
			PlasmaCore.ToolTipArea {
				anchors.fill: parent
				mainText: i18n("Kommand")
				subText: i18nc("@info", "Run voice kommands.")
			}
			MouseArea {
				id: mouseArea
				anchors.fill: parent
				onClicked: {
					// console.log("click...", command);
					if(status){
						toggle();
						shell.kill(command);
						defaultIcon.source = mic_off;
					}else{
						toggle();
						shell.run(command);
						defaultIcon.source = mic_on;
					}
				}
			}
	}
	Component.onCompleted: {
		// console.log(localPath);
	}
	PlasmaCore.DataSource {
		id: shell
		engine: 'executable'

		connectedSources: []

		function run(cmd){
			shell.connectSource(cmd);
		}
		
		function kill(cmd){
			shell.disconnectSource(cmd);
		}
		
		onSourceAdded: {
			//print(source)
		}

		onNewData: {
			var exitCode = data["exit code"]
			var exitStatus = data["exit status"]
			var stdout = data["stdout"]
			var stderr = data["stderr"]
			// console.log(exitCode, exitStatus, stdout, stderr);
			shell.disconnectSource(sourceName);
			if(exitCode == 2){
				if(defaultIcon.source == main.mic_on){
					mouseArea.clicked(null);
				}
			}
		}
	}
}