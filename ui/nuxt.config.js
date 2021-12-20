export default {
  ssr: false,
  target: "static",

  buildModules: ["@nuxtjs/vuetify"],
  modules: ["@nuxtjs/axios"],

  components: true,

  axios: {
    baseURL: process.env.API_URL || "http://localhost:8000/",
    browserBaseURL: process.env.API_URL || "http://localhost:8000/",
  },
};
