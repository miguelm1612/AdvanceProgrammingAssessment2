from PyQt6.QtWidgets import QDialog, QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, \
QPushButton, QLineEdit, QComboBox, QMessageBox, QHeaderView, QWidget
from PyQt6.QtCore import Qt, QTimer, QModelIndex
from PyQt6.QtGui import QFont, QColor, QBrush, QStandardItemModel, QStandardItem
import sys
import random
import json
from datetime import datetime
from DataFile import generate_licensee_data
from Housing_allocation import Ui_Dialog


class HousingAllocationApp(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Housing Allocation System")

        #Creates the RHU data
        self.initialize_rhu_data()

        #this loads the data that is needed but to 50
        try:
            self.data = generate_licensee_data(4000)
        except Exception as e:
            print(f"Error generating data: {e}")
            #this help create a backup data if the main doesn't work
            self.data = self.create_fallback_data(4000)

        self.current_page = 0
        self.records_per_page = 10


        self.selected_prisoner = None

        #most of this code is to help show the page by using an index as it is a stacked widget
        self.DashBoard.clicked.connect(lambda: self.show_page(0))
        self.Licenses.clicked.connect(lambda: self.show_page(1))
        self.RHUs.clicked.connect(lambda: self.show_page(2))
        self.Allocations.clicked.connect(lambda: self.show_page(3))
        self.Releases.clicked.connect(lambda: self.show_releases())
        self.Costs.clicked.connect(lambda: self.show_costs())
        self.Reports.clicked.connect(lambda: self.show_reports())

        self.setup_tables()

        self.Licenses.clicked.connect(self.populate_tables)

        if hasattr(self, 'pushButton'):
            self.pushButton.clicked.connect(self.show_selected_prisoner_details)

        if hasattr(self, 'pushButton_4'):
            self.pushButton_4.clicked.connect(lambda: self.show_page(1))

        self.setup_table_selection()

        if hasattr(self, 'pushButton_5'):
            self.pushButton_5.clicked.connect(self.sign_out)

        self.Allocations.clicked.connect(self.populate_prisoner_combo)

        if hasattr(self, 'comboBox1'):
            self.comboBox1.currentIndexChanged.connect(self.display_prisoner_requirements)

        #sets the window size
        self.setMinimumSize(700, 638)

        #By putting the index at 0 it helps shows the main page
        self.show_page(0)

    def initialize_rhu_data(self):
        #data for the RHU matches
        self.all_rhus = [
            {
                "name": "Hope Hostel - Strict",
                "location": "London",
                "cost": "£450",
                "beds": "4",
                "features": ["Curfew enforced", "Alcohol-free zone", "Regular drug testing", "Exclusion zones",
                             "24/7 monitoring"],
                "security": "Strict",
                "condition_support": ["curfew required", "restrict alcohol", "drug search", "exclusion zones required"]
            },
            {
                "name": "Bridge House - Moderate",
                "location": "Manchester",
                "cost": "£380",
                "beds": "2",
                "features": ["Alcohol-free", "Counseling available", "Work programs", "Evening curfew"],
                "security": "Moderate",
                "condition_support": ["restrict alcohol", "curfew required"]
            },
            {
                "name": "Pathway Lodge - Drug Focus",
                "location": "Birmingham",
                "cost": "£520",
                "beds": "3",
                "features": ["Daily drug testing", "Rehab programs", "Strict curfew", "No-visitor zones"],
                "security": "Strict",
                "condition_support": ["drug search", "curfew required", "exclusion zones required"]
            },
            {
                "name": "New Start Hostel - General",
                "location": "Leeds",
                "cost": "£410",
                "beds": "5",
                "features": ["Counseling available", "Work programs", "Education support", "Weekly check-ins"],
                "security": "Moderate",
                "condition_support": []
            },
            {
                "name": "Second Chance - High Security",
                "location": "Liverpool",
                "cost": "£390",
                "beds": "1",
                "features": ["Daily searches", "Mandatory drug tests", "Strict curfew", "Controlled zones"],
                "security": "High",
                "condition_support": ["drug search", "curfew required", "exclusion zones required"]
            },
            {
                "name": "Freedom House - Low Security",
                "location": "Bristol",
                "cost": "£350",
                "beds": "6",
                "features": ["Self-reporting", "Community service", "Day programs"],
                "security": "Low",
                "condition_support": []
            },
            {
                "name": "Horizon Home - Alcohol Focus",
                "location": "Glasgow",
                "cost": "£420",
                "beds": "3",
                "features": ["Strict alcohol ban", "AA meetings", "Breathalyzer tests", "Evening curfew"],
                "security": "Moderate",
                "condition_support": ["restrict alcohol", "curfew required"]
            },
            {
                "name": "Sunrise Shelter - All Conditions",
                "location": "Cardiff",
                "cost": "£480",
                "beds": "4",
                "features": ["Full surveillance", "Drug/alcohol testing", "Exclusion mapping", "Strict curfew"],
                "security": "High",
                "condition_support": ["curfew required", "restrict alcohol", "drug search", "exclusion zones required"]
            }
        ]

    def create_fallback_data(self, num_records):
        data = []
        first_names = ['John', 'Jane', 'Robert', 'Mary', 'David', 'Sarah', 'Michael', 'Lisa',
                       'James', 'Emma', 'William', 'Olivia', 'Richard', 'Sophia']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller']


        all_conditions = ['curfew required', 'restrict alcohol', 'exclusion zones required', 'drug search']

        #Create more varied condition sets
        for i in range(num_records):
            #Random number of conditions (0 to 4)
            num_conditions = random.randint(0, 4)
            if num_conditions > 0:
                conditions = random.sample(all_conditions, num_conditions)
            else:
                conditions = []

            #Check is all the prisoners fit the conditions for specifications
            if i % 10 == 0:
                conditions = all_conditions.copy()
            elif i % 7 == 0:
                conditions = []
            elif i % 5 == 0:
                conditions = ['drug search', 'curfew required']
            elif i % 3 == 0:
                conditions = ['restrict alcohol', 'exclusion zones required']


            random.shuffle(conditions)

            record = {
                'Name': f"{random.choice(first_names)} {random.choice(last_names)}",
                'Prisoner ID': f"PR{100000 + i}",
                'Days Until Housing': random.randint(30, 365),
                'Risk Level': random.choice(['Low', 'Medium', 'High', 'Very High']),
                'Category': random.choice(['A', 'B', 'C', 'D']),
                'Status': random.choice(['Pending', 'Approved', 'Denied', 'In Review']),
                'Conditions': conditions,
                'Offense Type': random.choice(['Burglary', 'Assault', 'Drug Offense', 'Fraud', 'Theft', 'Violence']),
                'Allocation Priority': random.randint(1, 100)
            }
            data.append(record)

        print(f"Created {len(data)} fallback records")
        return data

    def populate_prisoner_combo(self):
        if not hasattr(self, 'comboBox1'):
            print("No combobox1 found")
            return


        self.comboBox1.clear()

        #add the prisoners to combobox1
        for prisoner in self.data:
            self.comboBox1.addItem(prisoner['Name'])

        print(f"Populated combobox with {len(self.data)} prisoner names")


        self.populate_rhu_table()

    def populate_rhu_table(self):
        if not hasattr(self, 'tableViewten'):
            return


        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(
            ["RHU Name", "Location", "Weekly Cost", "Beds", "Match %", "Security", "Features"])

        #This shows all the RHUs with their titles next to them
        for rhu in self.all_rhus:
            row_items = [
                QStandardItem(rhu["name"]),
                QStandardItem(rhu["location"]),
                QStandardItem(rhu["cost"]),
                QStandardItem(rhu["beds"]),
                QStandardItem("--%"),
                QStandardItem(rhu["security"]),
                QStandardItem(", ".join(rhu["features"][:2]))
            ]
            model.appendRow(row_items)


        self.tableViewten.setModel(model)


        self.tableViewten.setColumnWidth(0, 140)
        self.tableViewten.setColumnWidth(1, 90)
        self.tableViewten.setColumnWidth(2, 85)
        self.tableViewten.setColumnWidth(3, 60)
        self.tableViewten.setColumnWidth(4, 70)
        self.tableViewten.setColumnWidth(5, 75)
        self.tableViewten.setColumnWidth(6, 150)


        self.tableViewten.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def display_prisoner_requirements(self, index):
        if index < 0 or index >= len(self.data):
            return

        prisoner = self.data[index]
        print(f"\nSelected prisoner: {prisoner['Name']}")
        print(f"Conditions: {prisoner.get('Conditions', [])}")

        #Format the requirements text
        requirements_text = f"<b>Prisoner Requirements:</b><br>"
        requirements_text += f"<b>Name:</b> {prisoner['Name']}<br>"
        requirements_text += f"<b>ID:</b> {prisoner['Prisoner ID']}<br>"
        requirements_text += f"<b>Risk Level:</b> {prisoner['Risk Level']}<br>"
        requirements_text += f"<b>Offense:</b> {prisoner.get('Offense Type', 'Unknown')}<br>"
        requirements_text += f"<b>Days Until Housing:</b> {prisoner['Days Until Housing']}<br>"
        requirements_text += f"<b>Priority Score:</b> {prisoner.get('Allocation Priority', 'N/A')}<br><br>"


        conditions = prisoner.get('Conditions', [])
        if conditions:
            requirements_text += f"<b>License Conditions ({len(conditions)}):</b><br>"
            for condition in conditions:
                requirements_text += f"• {condition}<br>"
        else:
            requirements_text += f"<b>License Conditions:</b> None<br>"


        if hasattr(self, 'label_19'):
            self.label_19.setText(requirements_text)
            self.label_19.setWordWrap(True)

        #This will update the prisoners match with the RHU
        self.update_rhu_matches_for_prisoner(prisoner)

        #places the top 3 matches it can find
        try:
            top_matches = self.get_top_rhu_matches(prisoner, 3)
            if top_matches:
                requirements_text += f"<br><b>Top RHU Recommendations:</b><br>"
                for i, match in enumerate(top_matches, 1):
                    color = self.get_match_color(match["match_score"])
                    requirements_text += f"{i}. <span style='color:{color};'><b>{match['name']}</b> - {match['match_score']}% match</span><br>"
                    requirements_text += f"   Location: {match['location']} | Cost: {match['cost']}/week<br>"
                    requirements_text += f"   Best for: {match['best_for']}<br><br>"


                if hasattr(self, 'label_19'):
                    self.label_19.setText(requirements_text)
        except AttributeError as e:
            print(f"Error getting top matches: {e}")

            if not hasattr(self, 'all_rhus'):
                self.initialize_rhu_data()

    def update_rhu_matches_for_prisoner(self, prisoner):
        #it matches the percentage with the prisoner
        if not hasattr(self, 'tableViewten') or not hasattr(self, 'all_rhus'):
            return

        model = self.tableViewten.model()
        if not model:
            return

        conditions = prisoner.get('Conditions', [])

        for row in range(model.rowCount()):
            rhu = self.all_rhus[row]
            match_score = self.calculate_detailed_match_score(conditions, rhu)

            #Update the match percentage cell
            match_item = QStandardItem(f"{match_score}%")

            #Apply color based on match score
            color = self.get_match_color(match_score)

            if color.startswith("#"):
                qcolor = QColor(color)
            else:
                qcolor = QColor(0, 0, 0)
            match_item.setForeground(QBrush(qcolor))


            if match_score >= 80:
                font = QFont()
                font.setBold(True)
                match_item.setFont(font)

            model.setItem(row, 4, match_item)

            #Also update features to show relevant ones
            relevant_features = self.get_relevant_features(conditions, rhu["features"])
            if len(relevant_features) > 2:
                features_text = ", ".join(relevant_features[:3]) + "..."
            else:
                features_text = ", ".join(relevant_features) if relevant_features else "General accommodation"

            features_item = QStandardItem(features_text)
            model.setItem(row, 6, features_item)

    def calculate_detailed_match_score(self, prisoner_conditions, rhu):
        rhu_supported_conditions = rhu.get("condition_support", [])
        rhu_features = rhu["features"]

        #Base score starts at 50%
        match_score = 50

        #Checks if the prisoner is compatible with the RHU
        for condition in prisoner_conditions:
            condition_lower = condition.lower()

            #Check if RHU explicitly supports this condition
            if any(supported_cond.lower() in condition_lower for supported_cond in rhu_supported_conditions):
                match_score += 15
            else:
                #Check for feature matches
                if "curfew" in condition_lower and any("curfew" in feature.lower() for feature in rhu_features):
                    match_score += 12
                elif "alcohol" in condition_lower and any("alcohol" in feature.lower() for feature in rhu_features):
                    match_score += 12
                elif "drug" in condition_lower and any("drug" in feature.lower() for feature in rhu_features):
                    match_score += 12
                elif "exclusion" in condition_lower and any(
                        "exclusion" in feature.lower() or "zone" in feature.lower() for feature in rhu_features):
                    match_score += 12
                else:

                    match_score -= 5


        risk_level = "High"  #Default
        if hasattr(self, 'selected_prisoner') and self.selected_prisoner:
            risk_level = self.selected_prisoner.get('Risk Level', 'Medium')

        #Adjust score based on risk level vs security
        if risk_level == "High" and rhu["security"] in ["High", "Strict"]:
            match_score += 10
        elif risk_level == "Medium" and rhu["security"] == "Moderate":
            match_score += 8
        elif risk_level == "Low" and rhu["security"] in ["Low", "Moderate"]:
            match_score += 6


        match_score += random.randint(-3, 3)

        #Ensures score is between 0 and 100
        match_score = max(0, min(100, match_score))

        return match_score

    def get_top_rhu_matches(self, prisoner, num_matches=3):
        conditions = prisoner.get('Conditions', [])
        matches = []

        for rhu in self.all_rhus:
            match_score = self.calculate_detailed_match_score(conditions, rhu)

            #Will determine which is the best RHU for the prisoner
            best_for = "General accommodation"
            if rhu.get("condition_support"):
                if len(rhu["condition_support"]) == 4:
                    best_for = "All conditions"
                elif "drug search" in rhu["condition_support"] and "curfew required" in rhu["condition_support"]:
                    best_for = "Drug-related offenses"
                elif "restrict alcohol" in rhu["condition_support"]:
                    best_for = "Alcohol-related offenses"
                elif "exclusion zones required" in rhu["condition_support"]:
                    best_for = "Geographic restrictions"

            matches.append({
                "name": rhu["name"],
                "match_score": match_score,
                "location": rhu["location"],
                "cost": rhu["cost"],
                "best_for": best_for,
                "security": rhu["security"]
            })


        matches.sort(key=lambda x: x["match_score"], reverse=True)

        return matches[:num_matches]

    def get_match_color(self, match_score):
        if match_score >= 90:
            return "#006400"
        elif match_score >= 80:
            return "#228B22"
        elif match_score >= 70:
            return "#32CD32"
        elif match_score >= 60:
            return "#FFD700"
        elif match_score >= 50:
            return "#FFA500"
        elif match_score >= 40:
            return "#FF8C00"
        else:
            return "#FF4500"

    def get_relevant_features(self, conditions, rhu_features):
        relevant = []

        for condition in conditions:
            condition_lower = condition.lower()
            for feature in rhu_features:
                feature_lower = feature.lower()

                if "curfew" in condition_lower and "curfew" in feature_lower:
                    relevant.append(feature)
                elif "alcohol" in condition_lower and "alcohol" in feature_lower:
                    relevant.append(feature)
                elif "drug" in condition_lower and "drug" in feature_lower:
                    relevant.append(feature)
                elif "exclusion" in condition_lower and ("exclusion" in feature_lower or "zone" in feature_lower):
                    relevant.append(feature)


        relevant = list(dict.fromkeys(relevant))


        if not relevant:
            relevant = rhu_features[:2]

        return relevant

    def setup_tables(self):
        tables = []

        #Check which tables exist in the ui
        if hasattr(self, 'nametable'):
            tables.append(('nametable', 'Name Table'))
        if hasattr(self, 'nametable_2'):
            tables.append(('nametable_2', 'Prisoner ID Table'))
        if hasattr(self, 'nametable_3'):
            tables.append(('nametable_3', 'Days Table'))
        if hasattr(self, 'nametable_4'):
            tables.append(('nametable_4', 'Risk Table'))

        for table_name, table_desc in tables:
            table = getattr(self, table_name)

            #Sets up table properties
            if hasattr(table, 'setModel'):
                model = QStandardItemModel(0, 1)
                table.setModel(model)


                table.verticalHeader().setVisible(False)
                table.horizontalHeader().setVisible(False)


                table.setColumnWidth(0, 131)


                table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

                #Set selection behavior
                table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
                table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

                #Set a clean style
                table.setStyleSheet("""
                    QTableView {
                        background-color: white;
                        border: 1px solid #d0d0d0;
                        gridline-color: #f0f0f0;
                    }
                    QTableView::item {
                        padding: 5px;
                    }
                """)

    def setup_table_selection(self):
        if hasattr(self, 'nametable'):
            #Connect selection change signal
            self.nametable.selectionModel().selectionChanged.connect(self.on_name_selected)

    def on_name_selected(self, selected, deselected):
        if not selected.indexes():
            return

        #Get the selected row index
        selected_index = selected.indexes()[0]
        row = selected_index.row()

        #Helps calculate the first index of the data
        start_idx = self.current_page * self.records_per_page
        actual_idx = start_idx + row

        if actual_idx < len(self.data):
            #Store the selected prisoner data
            self.selected_prisoner = self.data[actual_idx]

            #Highlight the corresponding rows in other tables
            self.highlight_other_tables(row)

            print(f"Selected prisoner: {self.selected_prisoner['Name']}")

    def highlight_other_tables(self, row):
        tables = []
        if hasattr(self, 'nametable_2'):
            tables.append(self.nametable_2)
        if hasattr(self, 'nametable_3'):
            tables.append(self.nametable_3)
        if hasattr(self, 'nametable_4'):
            tables.append(self.nametable_4)

        for table in tables:
            table.selectionModel().clearSelection()
            if row < table.model().rowCount():
                table.selectRow(row)
                #Scroll to the row if needed
                table.scrollTo(table.model().index(row, 0))

    def show_selected_prisoner_details(self):
        if not self.selected_prisoner:
            QMessageBox.warning(self, "No Selection", "Please select a prisoner first!")
            return

        self.show_page(2)
        self.populate_prisoner_details()

    def populate_prisoner_details(self):
        if not self.selected_prisoner:
            return

        #will update prisoner details if they exist
        try:
            #Check if these labels exist and update them
            if hasattr(self, 'label_8'):
                self.label_8.setText(f"Name: {self.selected_prisoner['Name']}")
            if hasattr(self, 'label_9'):
                self.label_9.setText(f"ID: {self.selected_prisoner['Prisoner ID']}")
            if hasattr(self, 'label_10'):
                self.label_10.setText(f"Status: {self.selected_prisoner.get('Status', 'Unknown')}")
            if hasattr(self, 'label_11'):
                #This might be the title label
                self.label_11.setText(f"Prisoner Details: {self.selected_prisoner['Name']}")
        except Exception as e:
            print(f"Error updating labels: {e}")

        #updates the check boxes if they have been ticked
        self.update_conditions_checkboxes()

    def update_conditions_checkboxes(self):
        if not self.selected_prisoner:
            return

        #Get conditions from prisoner data
        conditions = self.selected_prisoner.get('Conditions', [])

        #Update checkboxes if they exist
        checkbox_mapping = {
            'curfew required': getattr(self, 'condition1check', None),
            'restrict alcohol': getattr(self, 'condition2check', None),
            'exclusion zones required': getattr(self, 'condition3check', None),
            'drug search': getattr(self, 'condition4check', None)
        }

        for condition_text, checkbox in checkbox_mapping.items():
            if checkbox:
                checkbox.setChecked(condition_text in conditions)
                #Don't change the text if it's already set
                if checkbox.text() == "":
                    checkbox.setText(condition_text.capitalize())

    def populate_tables(self):
        if not self.data:
            QMessageBox.warning(self, "No Data", "No data available to display.")
            return

        #Get data for current page
        start_idx = self.current_page * self.records_per_page
        end_idx = min(start_idx + self.records_per_page, len(self.data))
        page_data = self.data[start_idx:end_idx]

        #Extract data for each column
        names = [record['Name'] for record in page_data]
        prisoner_ids = [record['Prisoner ID'] for record in page_data]
        days_until_housing = [str(record['Days Until Housing']) for record in page_data]
        risk_levels = [record['Risk Level'] for record in page_data]

        #this adds any data onto the nametables which will help display
        if hasattr(self, 'nametable'):
            self.populate_single_table(self.nametable, names)
        if hasattr(self, 'nametable_2'):
            self.populate_single_table(self.nametable_2, prisoner_ids)
        if hasattr(self, 'nametable_3'):
            self.populate_single_table(self.nametable_3, days_until_housing)
        if hasattr(self, 'nametable_4'):
            self.populate_single_table_with_risk_colors(self.nametable_4, risk_levels)

    def populate_single_table(self, table, data):
        if not table or not hasattr(table, 'model'):
            return


        model = table.model()
        if model is None:
            model = QStandardItemModel(0, 1)
            table.setModel(model)
        else:
            model.removeRows(0, model.rowCount())


        for row, value in enumerate(data):
            item = QStandardItem(str(value))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setForeground(QBrush(QColor(0, 0, 0)))  #Black text
            model.appendRow([item])


        table.resizeRowsToContents()

    def populate_single_table_with_risk_colors(self, table, risk_levels):
        if not table or not hasattr(table, 'model'):
            return

        #this Clears any data made
        model = table.model()
        if model is None:
            model = QStandardItemModel(0, 1)
            table.setModel(model)
        else:
            model.removeRows(0, model.rowCount())


        for row, risk in enumerate(risk_levels):
            item = QStandardItem(str(risk))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)


            text_color = self.get_risk_text_color(risk)
            item.setForeground(QBrush(text_color))

            model.appendRow([item])

        #this just resizes the rows
        table.resizeRowsToContents()

    def get_risk_text_color(self, risk_level):

        colors = {
            'Very High': QColor(178, 34, 34),
            'High': QColor(220, 20, 60),
            'Medium': QColor(218, 165, 32),
            'Low': QColor(60, 179, 113)
        }
        return colors.get(risk_level, QColor(0, 0, 0))

    def filter_data(self):
        try:
            self.data = generate_licensee_data(50)
        except:
            self.data = self.create_fallback_data(50)

        self.populate_tables()
        QMessageBox.information(self, "Search", "Data refreshed with new records!")

    def show_page(self, page_index):
        if hasattr(self, 'LicenseDetails2'):
            self.LicenseDetails2.setCurrentIndex(page_index)

            #this page updates and shows licenses page
            if page_index == 1:
                self.populate_tables()

                self.selected_prisoner = None
                if hasattr(self, 'nametable'):
                    self.nametable.selectionModel().clearSelection()
            elif page_index == 0:
                self.update_dashboard_stats()
            elif page_index == 3:
                self.populate_prisoner_combo()
                #this updates a prisoner if they were selected
                if hasattr(self, 'comboBox1') and self.comboBox1.currentIndex() >= 0:
                    self.display_prisoner_requirements(self.comboBox1.currentIndex())

    def update_dashboard_stats(self):
        if not self.data:
            return


        total_prisoners = len(self.data)
        pending = sum(1 for record in self.data if record.get('Days Until Housing', 0) > 180)
        allocated = sum(1 for record in self.data if record.get('Days Until Housing', 0) <= 180)


        if hasattr(self, 'pendingLicensesOut_3'):
            self.pendingLicensesOut_3.setText(str(pending))
        if hasattr(self, 'AllocatedLicensesOut_3'):
            self.AllocatedLicensesOut_3.setText(str(allocated))
        if hasattr(self, 'ExitedLicenesesOut_3'):
            self.ExitedLicenesesOut_3.setText("0")  #Example - you can modify this

        high_risk = sum(1 for record in self.data if record.get('Risk Level', '') in ['High', 'Very High'])
        alert_text = f"High Risk Prisoners: {high_risk}\nPending Housing: {pending}"

        #if the label exits it uses it for alerts
        if hasattr(self, 'Alerts'):
            self.Alerts.setText(alert_text)

    def show_releases(self):
        #shows release page but
        QMessageBox.information(self, "Releases", "Releases functionality not implemented yet")

    def show_costs(self):
        #shows the cost pag ebut is not functional just yet
        QMessageBox.information(self, "Costs", "Costs functionality not implemented yet")

    def show_reports(self):
        #shows the report page that appears on screen
        QMessageBox.information(self, "Reports", "Reports functionality not implemented yet")

    def sign_out(self):
        #this does the sign out page
        reply = QMessageBox.question(self, 'Sign Out',
                                     'Are you sure you want to sign out?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Signed Out", "You have been signed out.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    housing_allocation = HousingAllocationApp()
    housing_allocation.show()
    sys.exit(app.exec())