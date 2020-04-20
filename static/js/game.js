function subscribe(url){
    axios.post("/game")
    .then(function (response) {
        console.log(response);
        if(response.data.action == "end") return;
        setTimeout(function(){subscribe(url)}, 999);
    })
    .catch(function (error) {
        console.log(error);
        setTimeout(function(){subscribe(url)}, 1000);
    });
}

subscribe("/game")