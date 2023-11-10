

function home(){
    window.location.href = '/'
}


function switchmenu(){

    const element = document.getElementById('plside');
    if (element.style.display == ""){
        element.style.display = "block";
    }else{
        element.style.display = "";
    }
}

function checklogin(){
    const status = document.getElementById('login').value;

   
    if (status == 'Login'){

        document.getElementById('login').value = 'Log Out';
    }
    else{
        document.getElementById('login').value = 'Login';
    }
    alert(status)
}

async function signup(){
    const response = await fetch('/login', {method: 'POST'})
}


function toggleMenu(){
    // alert('got here');
   
        const element = document.getElementById('respNav');

        if (element.style.display == "none" || element.style.display ==""){
            element.style.display = "block";
        }
        else {
            element.style.display = "none";
        }

      
    

    }

    const windowWidth = window.innerWidth;
    const element2 = document.getElementById('section2ImgContainer');

 if (windowWidth < 1099){
            element2.style.display = "none";
            // alert(windowWidth);
        } else{
            element2.style.display = "flex";
        }

  
    function handleWindow(){
        const element = document.getElementById('respNav');
        const windowWidth = window.innerWidth;

        const element2 = document.getElementById('section2ImgContainer')

        if (windowWidth  >= 920){

            element.style.display = "none";
            // alert(windowWidth);
            
        }
        
        if (windowWidth < 1099){
            element2.style.display = "none";
            // alert(windowWidth);
        } else{
            // element2.style.display = "flex";
        }

        // alert(windowWidth);
        

    }

    window.addEventListener('resize', handleWindow)




    document.querySelectorAll('.contentHolder3').forEach((content, index) => {
        content.addEventListener('scroll', function () {
          const scrollPosition = this.scrollLeft;
          const indicators = document.getElementById('.scrollContainer');
      
          indicators.forEach((indicator, i) => {
            if (i === index) {
              indicator.style.backgroundColor = 'blue'; // Change to the desired color
            } else {
              indicator.style.backgroundColor = '#ccc'; // Reset to default color
            }
          });
        });
      });
      