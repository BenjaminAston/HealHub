document.addEventListener("DOMContentLoaded", () => {
    class WorkoutTracker {
        static LOCAL_STORAGE_DATA_KEY = "workout-tracker-entries";

        constructor(root) {
            this.root = root;
            this.root.innerHTML = WorkoutTracker.html(); // Clear the root before inserting HTML
            this.entries = [];

            this.loadEntries();
            this.updateView();

            // Add event listener for "Add Entry" button
            this.root.querySelector(".tracker__add").addEventListener("click", () => {
                const date = new Date();
                const year = date.getFullYear();
                const month = (date.getMonth() + 1).toString().padStart(2, "0");
                const day = date.getDate().toString().padStart(2, "0");

                this.addEntry({
                    date: `${year}-${month}-${day}`,
                    workout: "walking",
                    duration: 30
                });
            });
        }

        static html() {
            return `
                <table class="tracker">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Workout</th>
                            <th>Duration</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody class="tracker__entries"></tbody>
                    <tfoot>
                        <tr class="tracker__row tracker__row--add">
                            <td colspan="4">
                                <span class="tracker__add">Add Entry &plus;</span>
                            </td>
                        </tr>
                    </tfoot>
                </table>
            `;
        }

        static rowHtml() {
            return `
                <tr class="tracker__row">
                    <td>
                        <input type="date" class="tracker__date">
                    </td>
                    <td>
                        <select class="tracker__workout">
                            <option value="promenera">Promenera</option>
                            <option value="Springa">Springa</option>
                            <option value="cykla-utomhus">Cykla Utomhus</option>
                            <option value="Cykla-inomhus">Cykla Innomhus</option>
                            <option value="Simma">Simma</option>
                            <option value="yoga">Yoga</option>
                            <option value="rehab-nacke">Rehab Nacke</option>
                            <option value="rehab-armar">Rehab Armar</option>
                            <option value="rehab-armbåge">Rehab Armbåge</option>
                            <option value="rehab-händer">Rehab Händer</option>
                            <option value="rehab-bröst">Rehab Bröst</option>
                            <option value="rehab-mage">Rehab Mage</option>
                            <option value="rehab-ben">Rehab Ben</option>
                            <option value="rehab-knä">Rehab Knä</option>
                            <option value="rehab-fot">Rehab Fot</option>
                        </select>
                    </td>
                    <td>
                        <input type="number" class="tracker__duration">
                        <span class="tracker__text">minutes</span>
                    </td>
                    <td>
                        <button type="button" class="tracker__button tracker__delete">&times;</button>
                    </td>
                </tr>
            `;
        }

        loadEntries() {
            this.entries = JSON.parse(localStorage.getItem(WorkoutTracker.LOCAL_STORAGE_DATA_KEY) || "[]");
        }

        saveEntries() {
            localStorage.setItem(WorkoutTracker.LOCAL_STORAGE_DATA_KEY, JSON.stringify(this.entries));
        }

        updateView() {
            const tableBody = this.root.querySelector(".tracker__entries");

            tableBody.querySelectorAll(".tracker__row").forEach(row => {
                row.remove();
            });

            this.entries.forEach(data => this.addRow(data));
        }

        addRow(data) {
            const template = document.createElement("template");
            let row = null;

            template.innerHTML = WorkoutTracker.rowHtml().trim();
            row = template.content.firstElementChild;

            row.querySelector(".tracker__date").value = data.date;
            row.querySelector(".tracker__workout").value = data.workout;
            row.querySelector(".tracker__duration").value = data.duration;

            row.querySelector(".tracker__date").addEventListener("change", ({ target }) => {
                data.date = target.value;
                this.saveEntries();
            });

            row.querySelector(".tracker__workout").addEventListener("change", ({ target }) => {
                data.workout = target.value;
                this.saveEntries();
            });

            row.querySelector(".tracker__duration").addEventListener("change", ({ target }) => {
                data.duration = target.value;
                this.saveEntries();
            });

            row.querySelector(".tracker__delete").addEventListener("click", () => {
                this.deleteEntry(data);
            });

            this.root.querySelector(".tracker__entries").appendChild(row);
        }

        addEntry(data) {
            this.entries.push(data);
            this.saveEntries();
            this.updateView();
        }

        deleteEntry(dataToDelete) {
            this.entries = this.entries.filter(data => data !== dataToDelete);
            this.saveEntries();
            this.updateView();
        }
    }

    const app = document.getElementById("app");

    const wt = new WorkoutTracker(app);

    window.wt = wt; // For debugging purposes
});
