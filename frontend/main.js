
var app = new Vue({
    el: '#app',
    data: {
      message: 'Hello Vue!',
      functions: [],
      url: ""
    },
    methods: {
        getFunctions: function() {
            this.$http.get("http://localhost:8080/funcs").then(function(response){
                console.log(response);
                this.functions = response.body;
            }, function(error){
                console.log(error.statusText);
            });
        },
        newSite: function(url) {
            console.log(url);
            this.$http.get("http://localhost:8080/create?url=" + url).then(function(response) {
                console.log(response);
                window.location.reload();
            }, function(error){
                console.log(error);
            })
        }
    },
    mounted: function () {
        this.getFunctions();
    }

  })