import QtQuick 2.0
import QtQuick.Controls 2.5 as QtControls
import QtQuick.Layouts 1.15

import org.kde.kirigami 2.5 as Kirigami
import org.kde.plasma.plasmoid 2.0
import org.kde.plasma.core 2.0 as PlasmaCore

ColumnLayout {
	id: main

	property alias cfg_language: language.currentValue
	property alias cfg_localPath: localPath.text

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
			}
		}
	}

	Kirigami.FormLayout {
		id: generalConfigPage
		anchors.fill: parent

		Kirigami.Separator {
			Kirigami.FormData.label: i18nc("@title:group", "Global")
			Kirigami.FormData.isSection: true
		}

		RowLayout {
			Kirigami.FormData.label: i18n("Local Path:")
			QtControls.TextField {
				id: localPath
				enabled: true
				visible: true
			}
		}

		RowLayout {
			Kirigami.FormData.label: i18n("Language:")
			QtControls.ComboBox {
				id: language
				enabled: true
				visible: true
				textRole: "label"
				valueRole: "value"
				model: [
					{"label": i18n("alemão"), "value": "de"},
					{"label": i18n("amárico"), "value": "am"},
					{"label": i18n("árabe"), "value": "ar"},
					{"label": i18n("basco"), "value": "eu"},
					{"label": i18n("bengalês"), "value": "bn"},
					{"label": i18n("búlgaro"), "value": "bg"},
					{"label": i18n("canarês"), "value": "kn"},
					{"label": i18n("catalão"), "value": "ca"},
					{"label": i18n("cherokee"), "value": "chr"},
					{"label": i18n("chinês"), "value": "zh-CN"},
					{"label": i18n("coreano"), "value": "ko"},
					{"label": i18n("croata"), "value": "h"},
					{"label": i18n("dinamarquês"), "value": "da"},
					{"label": i18n("eslovaco"), "value": "sk"},
					{"label": i18n("esloveno"), "value": "sl"},
					{"label": i18n("espanhol"), "value": "es"},
					{"label": i18n("estoniano"), "value": "et"},
					{"label": i18n("filipino"), "value": "fil"},
					{"label": i18n("finlandês"), "value": "fi"},
					{"label": i18n("francês"), "value": "fr"},
					{"label": i18n("galês"), "value": "cy"},
					{"label": i18n("grego"), "value": "el"},
					{"label": i18n("guzerate"), "value": "gu"},
					{"label": i18n("hebraico"), "value": "iw"},
					{"label": i18n("hindi"), "value": "hi"},
					{"label": i18n("holandês"), "value": "nl"},
					{"label": i18n("húngaro"), "value": "hu"},
					{"label": i18n("indonésio"), "value": "id"},
					{"label": i18n("inglês"), "value": "en"},
					{"label": i18n("islandês"), "value": "is"},
					{"label": i18n("italiano"), "value": "it"},
					{"label": i18n("japonês"), "value": "ja"},
					{"label": i18n("letão"), "value": "lv"},
					{"label": i18n("lituano"), "value": "lt"},
					{"label": i18n("malaiala"), "value": "ml"},
					{"label": i18n("malaio"), "value": "ms"},
					{"label": i18n("marata"), "value": "mr"},
					{"label": i18n("norueguês"), "value": "não"},
					{"label": i18n("polonês"), "value": "pl"},
					{"label": i18n("portugal"), "value": "pt-PT"},
					{"label": i18n("português"), "value": "pt-BR"},
					{"label": i18n("reino unido"), "value": "en-GB"},
					{"label": i18n("romeno"), "value": "ro"},
					{"label": i18n("russo"), "value": "ru"},
					{"label": i18n("suaíli"), "value": "sw"},
					{"label": i18n("sueco"), "value": "sv"},
					{"label": i18n("sérvio"), "value": "sr"},
					{"label": i18n("tailandês"), "value": "th"},
					{"label": i18n("taiwan"), "value": "zh-TW"},
					{"label": i18n("tcheco"), "value": "cs"},
					{"label": i18n("turco"), "value": "tr"},
					{"label": i18n("tâmil"), "value": "ta"},
					{"label": i18n("télugo"), "value": "te"},
					{"label": i18n("ucraniano"), "value": "uk"},
					{"label": i18n("urdu"), "value": "ur"},
					{"label": i18n("vietnamita"), "value": "vi"},
				]
				onActivated: cfg_language = currentValue
				Component.onCompleted: {
					for (var i = 0; i < model.length; i++) {
						if (model[i]["value"] === Plasmoid.configuration.language) {
							language.currentIndex = i;
						}
					}
				}
			}
		}

		Kirigami.Separator {
			Kirigami.FormData.label: i18nc("@title:group", "Command group")
			Kirigami.FormData.isSection: true
		}

		RowLayout {
			QtControls.Button {
				text: i18nc("@action:button", "Configure")
				enabled: true
				onClicked: {
					console.log("configure...");
					// console.log(cfg_localPath);
					shell.run(" python3 "+cfg_localPath+"/contents/code/configure.py command ");
				}
			}
		}

		Kirigami.Separator {
			Kirigami.FormData.label: i18nc("@title:group", "Terminal group")
			Kirigami.FormData.isSection: true
		}

		RowLayout {
			QtControls.Button {
				text: i18nc("@action:button", "Configure")
				enabled: true
				onClicked: {
					console.log("configure...");
					// console.log(cfg_localPath);
					shell.run(" python3 "+cfg_localPath+"/contents/code/configure.py terminal ");
				}
			}
		}

	}

}