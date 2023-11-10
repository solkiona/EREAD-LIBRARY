function favorite(){

    const favorite = document.getElementById('favorite');

    let color = favorite.style.backgroundColor;

    if (color !== "red"){
        favorite.style.backgroundColor = "red";
        favorite.style.border= "none";
    }
    else{
        favorite.style.backgroundColor = "inherit";
        favorite.style.border= "1px solid black";
    }



}