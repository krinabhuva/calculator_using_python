const display = document.getElementById("display");

const buttons = document.querySelectorAll(".btn");

buttons.forEach(button => {
    button.addEventListener("click", () => {
        handleInput(button.dataset.value);
    });
});

function handleInput(value){

    if(value === "C"){
        display.value = "";
    }

    else if(value === "⌫"){
        display.value = display.value.slice(0, -1);
    }

    else if(value === "="){
        calculate();
    }

    else{
        display.value += value;
    }
}

async function calculate(){

    if(!display.value) return;

    try{

        const response = await fetch("/calculate",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                expression:display.value
            })
        });

        const data = await response.json();

        if(data.error){
            display.value = data.error;
        }
        else{
            display.value = data.result;
        }

    }catch(error){
        display.value = "Error";
    }
}

document.addEventListener("keydown",(e)=>{

    const allowed =
        "0123456789+-*/.%";

    if(allowed.includes(e.key)){
        display.value += e.key;
    }

    else if(e.key === "Backspace"){
        display.value =
            display.value.slice(0,-1);
    }

    else if(e.key === "Enter"){
        calculate();
    }

    else if(e.key === "Escape"){
        display.value = "";
    }
});