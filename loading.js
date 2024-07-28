load=document.querySelector(".loading");
window.addEventListener('DOMContentLoaded',()=>{
    setTimeout(()=>{
        console.log("loaded");
        load.style.display='none';
    },1000);
})