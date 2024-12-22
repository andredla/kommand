import QtQuick 2.0
import org.kde.plasma.configuration 2.0

ConfigModel {
	ConfigCategory {
		name: i18nc("@title", "Configuration")
		icon: "preferences-desktop-color"
		source: "configGeneral.qml"
	}
}
