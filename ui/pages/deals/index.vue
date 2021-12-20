<template>
  <div>
    <h1 class="mb-10">Deals</h1>

    <v-data-table
      v-if="deals"
      :headers="headers"
      :items="deals"
      :items-per-page="5"
      class="elevation-1"
    ></v-data-table>
  </div>
</template>

<script>
export default {
  name: "deals",
  data() {
    return {
      headers: [
        {
          text: "Name",
          align: "start",
          value: "name",
        },
        { text: "Modified", value: "modified" },
        { text: "Amount", value: "amount" },
        { text: "Closed", value: "closed" },
        { text: "Close date", value: "close_date" },
        { text: "Owner", value: "owner" },
      ],
      deals: undefined,
    };
  },
  created() {
    this.fetchDeals();
  },
  methods: {
    fetchDeals() {
      this.$axios.get("api/deals").then((response) => {
        this.deals = response.data.deals;
      });
    },
  },
};
</script>
