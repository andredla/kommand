import sys
import os
import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import Qt as qt
import sqlite3
import json
import base64

localPath = os.path.dirname(os.path.realpath(__file__))

class MainWindow(qtw.QWidget):
	def __init__(self):
		super().__init__()
		self.type = sys.argv[1]
		self.setWindowTitle("Kommand "+self.type+" configuration")
		self.setFixedWidth(800)
		self.setFixedHeight(800)
		self.setLayout(qtw.QVBoxLayout())
		self.dbMake()
		# self.dbGetAll()
		self.render()
		self.show()
		self.load()

	def dbMake(self):
		self.conn = sqlite3.connect(localPath+"/db.sqlite")
		self.cur = self.conn.cursor()
		self.cur.execute("CREATE TABLE IF NOT EXISTS database (id INTEGER PRIMARY KEY, type VARCHAR(25), command VARCHAR(25), json TEXT);")
		self.conn.commit()

		rows = self.dbGetType('command')
		if( len(rows) <= 0 ):
			self.cur.execute("INSERT INTO database (type, json) VALUES ('command', '')")
			self.conn.commit()

		rows = self.dbGetType('terminal')
		if( len(rows) <= 0 ):
			self.cur.execute("INSERT INTO database (type, json) VALUES ('terminal', '')")
			self.conn.commit()
		return True

	def dbGetType(self, type):
		self.cur.execute("select * from database where type = '"+type+"'")
		rows = self.cur.fetchall()
		return rows

	def bdSaveType(self, type, data, command):
		self.cur.execute("UPDATE database set command = '"+command+"', json = '"+data+"' where type = '"+type+"'")
		self.conn.commit()
		return True

	def dbGetAll(self):
		self.cur.execute("select * from database")
		rows = self.cur.fetchall()
		# lines = [description[0] for description in self.cur.description]
		# print(lines)
		for row in rows:
			print(row)
		return True

	def commandEncodeDecode(self, data, encdec):
		if encdec == "encode":
			return base64.b64encode(data.encode("ascii")).decode("ascii")
		if encdec == "decode":
			return base64.b64decode(data).decode("ascii")
		return True

	def addItem(self, obj):
		row = qtw.QWidget()
		row.setLayout(qtw.QHBoxLayout())

		word = qtw.QLineEdit()
		label_word = qtw.QLabel("Word:")
		word_widget = qtw.QWidget()
		word_widget.setLayout(qtw.QVBoxLayout())
		word_widget.layout().addWidget(label_word)
		word_widget.layout().addWidget(word)

		command = qtw.QLineEdit()
		label_command = qtw.QLabel("Execute:")
		command_widget = qtw.QWidget()
		command_widget.setLayout(qtw.QVBoxLayout())
		command_widget.layout().addWidget(label_command)
		command_widget.layout().addWidget(command)

		talk = qtw.QLineEdit()
		label_talk = qtw.QLabel("Talk:")
		talk_widget = qtw.QWidget()
		talk_widget.setLayout(qtw.QVBoxLayout())
		talk_widget.layout().addWidget(label_talk)
		talk_widget.layout().addWidget(talk)

		if obj:
			word.setText(obj["word"])
			command.setText(self.commandEncodeDecode(obj["command"], "decode"))
			talk.setText(obj["talk"])

		btn = qtw.QPushButton("Remove")
		btn.clicked.connect( lambda: self.removeItem(row) )
		label_btn = qtw.QLabel("Action:")
		btn_widget = qtw.QWidget()
		btn_widget.setLayout(qtw.QVBoxLayout())
		btn_widget.layout().addWidget(label_btn)
		btn_widget.layout().addWidget(btn)

		row.layout().addWidget(word_widget)
		row.layout().addWidget(command_widget)
		row.layout().addWidget(talk_widget)
		row.layout().addWidget(btn_widget)
		self.vbox.layout().addWidget(row)
		return True

	def removeItem(self, row):
		row.deleteLater()
		return True

	def save(self):
		json_arr = {"data": []}
		for a in range(0,self.vbox.layout().count()):
			row = self.vbox.layout().itemAt(a).widget()
			word = row.layout().itemAt(0).widget().layout().itemAt(1).widget().text()
			command = row.layout().itemAt(1).widget().layout().itemAt(1).widget().text()
			talk = row.layout().itemAt(2).widget().layout().itemAt(1).widget().text()
			# print(row.id, word, command, talk)
			obj = {}
			obj["word"] = word
			obj["command"] = self.commandEncodeDecode(command, "encode")
			obj["talk"] = talk
			json_arr["data"].append(obj)
		data = json.dumps(json_arr)
		self.bdSaveType(self.type, data, self.command.text())
		os.system("rm " + os.path.join(localPath, "audio", self.type, "*"))
		return True

	def load(self):
		rows = self.dbGetType(self.type)
		data = {"data": []}
		for row in rows:
			if row[2]:
				self.command.setText(row[2])
			if row[3]:
				data = json.loads(row[3])
		for row in data["data"]:
			self.addItem(row)
		return True

	def render(self):
		vw = qtw.QWidget()
		vw.setLayout(qtw.QVBoxLayout())

		self.command = qtw.QLineEdit()
		label_command = qtw.QLabel("Command:")
		command_widget = qtw.QWidget()
		command_widget.setLayout(qtw.QVBoxLayout())
		command_widget.layout().addWidget(label_command)
		command_widget.layout().addWidget(self.command)

		btn_add = qtw.QPushButton("Add",clicked = self.addItem)

		sc = qtw.QScrollArea()
		sc.setWidgetResizable(True)
		sc_widget = qtw.QWidget()
		self.vbox = qtw.QVBoxLayout()
		self.vbox.setAlignment(qt.AlignTop)
		sc_widget.setLayout(self.vbox)
		sc.setWidget(sc_widget)

		btn_save = qtw.QPushButton("Save",clicked = self.save)

		vw.layout().addWidget(command_widget)
		vw.layout().addWidget(btn_add)
		vw.layout().addWidget(sc)
		vw.layout().addWidget(btn_save)

		self.layout().addWidget(vw)

app = qtw.QApplication([])
mw = MainWindow()
app.exec_()