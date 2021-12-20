<template>
  <div>
    <v-data-table
      v-if="statement_compensations"
      :headers="headers"
      :items="statement_compensations"
      :items-per-page="5"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar
          class="mt-10"
          flat
        >
          <v-toolbar-title><h1 class="mb-2">Statement Compensations</h1></v-toolbar-title>
          <v-divider
            class="mx-4"
            inset
            vertical
          ></v-divider>
          <v-spacer></v-spacer>
          <v-dialog
            v-model="dialog"
            max-width="500px"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="primary"
                dark
                class="mb-2"
                v-bind="attrs"
                v-on="on"
              >
                New Statement Compensation
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="text-h5">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col
                      cols="12"
                      sm="6"
                      md="12"
                    >
                      <v-text-field
                        v-model="editedItem.compensation.name"
                        label="Name"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="6"
                    >
                    <v-combobox
                      v-model="editedItem.compensation.type"
                      :items="compensation_types"
                      label="Type"
                    ></v-combobox>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="6"
                    >
                      <v-menu
                        ref="dateMenu"
                        v-model="dateMenu"
                        :close-on-content-click="false"
                        :return-value.sync="dateToParse"
                        transition="scale-transition"
                        offset-y
                        min-width="auto"
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            v-model="dateToParse"
                            label="Date"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker
                          v-model="dateToParse"
                          type="month"
                          no-title
                          scrollable
                        >
                          <v-spacer></v-spacer>
                          <v-btn
                            text
                            color="primary"
                            @click="dateMenu = false"
                          >
                            Cancel
                          </v-btn>
                          <v-btn
                            text
                            color="primary"
                            @click="$refs.dateMenu.save(dateToParse)"
                          >
                            OK
                          </v-btn>
                        </v-date-picker>
                      </v-menu>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="12"
                    >
                    <v-autocomplete
                      v-if="executives"
                      v-model="editedItem.statement.executive"
                      :items="executives"
                      item-text="name"
                      item-value="id"
                      label="Executive"
                      clearable
                      dense
                    ></v-autocomplete>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="close"
                >
                  Cancel
                </v-btn>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="save"
                >
                  Save
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title class="text-h5">Are you sure you want to delete this item?</v-card-title>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
                <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:no-data>
        <div>No data</div>
      </template>
    </v-data-table>

    <v-snackbar
      v-model="successSnackbar"
      :timeout="snackbarTimeout"
    >
      {{ successText }}

      <template v-slot:action="{ attrs }">
        <v-btn
          color="blue"
          text
          v-bind="attrs"
          @click="successSnackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
export default {
  name: "statement_compensations",
  data() {
    return {
      headers: [
        {
          text: "Name",
          align: "start",
          value: "compensation.name",
        },
        { text: "Type", value: "compensation.type" },
        { text: "Executive", value: "statement.executive" },
        { text: "Month", value: "statement.month" },
        { text: "Year", value: "statement.year" },
        { text: "Amount", value: "amount" },
      ],
      statement_compensations: undefined,
      executives: undefined,
      compensation_types: ["Simple", "Complicated"],
      dateToParse: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 7),
      dialog: false,
      dateMenu: false,
      dialogDelete: false,
      successSnackbar: false,
      successText: "",
      snackbarTimeout: 2000,
      editedIndex: -1,
      editedItem: {
        compensation: {
          name: '',
          type: '',
        },
        statement: {
          month: 0,
          year: 0,
          executive: 0,
        },
        amount: 0,
      },
      defaultItem: {
        compensation: {
          name: '',
          type: '',
        },
        statement: {
          month: 0,
          year: 0,
          executive: 0,
        },
        amount: 0,
      },
    };
  },
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'New Statement Compensation' : 'Edit Statement Compensation'
    },
  },

  watch: {
    dialog (val) {
      val || this.close()
    },
    dialogDelete (val) {
      val || this.closeDelete()
    },
  },

  created() {
    this.fetchExecutives();
    this.fetchStatementCompensations();
  },
  methods: {
    fetchExecutives() {
      this.$axios.get("api/executives").then((response) => {
        this.executives = response.data.executives;
      });
    },
    fetchStatementCompensations() {
      this.$axios.get("api/statement_compensations").then((response) => {
        this.statement_compensations = response.data.statement_compensations;
      });
    },
    close () {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    closeDelete () {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    save () {
      this.editedItem.statement.year = parseInt(this.dateToParse.substr(0, 4))
      this.editedItem.statement.month = parseInt(this.dateToParse.substr(5, 6))
      if (this.editedIndex > -1) {
        Object.assign(this.statement_compensations[this.editedIndex], this.editedItem)
      } else {
        this.$axios.post("api/statement_compensations", this.editedItem).then((response) => {
          this.statement_compensations.push(response.data);
          this.successText = response.data.compensation.name + " Statement Compensation has been successfully created";
          this.successSnackbar = true;
        });
      }
      this.close()
    },
  },
};
</script>
