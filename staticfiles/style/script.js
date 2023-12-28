// login page

const hidden = document.querySelector(".emailbox");
const show = document.querySelector(".numbox");
const id = document.getElementById("num");
const mail = document.getElementById("email");


function fun() {
  hidden.classList.toggle("showff");
  show.classList.toggle("off");
}
function fun1() {
  show.classList.toggle("off");
  hidden.classList.toggle("showff");
}


// mail.addEventListener("click",()=>{

// })
// id.addEventListener("click",()=>{

// })

// <!-- Accordions  -->




// scroll properties
const postion = document.querySelectorAll(".postion-part");
const dot = document.querySelectorAll(".bi-dot");
for (let i = 0; i < dot.length; i++) {
  dot[i].addEventListener("click", (e) => {
    dot.forEach((show) => {
      show.style.color = 'gray';

    })
    dot[i].style.color = "#202020";

  });
}

const tablinks = document.querySelectorAll(".tablinks");

for (let i = 0; i < tablinks.length; i++) {
  tablinks[i].addEventListener("click", (e) => {
    tablinks.forEach((show) => {
      show.style.backgroundColor = 'gray';

    })
    tablinks[i].style.backgroundColor = "rgb(88, 85, 85)";
    tablinks[i].style.color = "white";

  });
}


// for(let x=0;x<dot.length;x++){
//   dot[x].addEventListener("click",()=>{
//     dot[x].style.color="#000";
//   })
// }
// window.addEventListener("scroll",()=>{
//   if(window.pageYOffset>950){
//     dot[1].style.color="#000"
//   }
// })
// window.addEventListener("scroll",()=>{
//   if(window.pageYOffset>1200){
//     dot[2].style.color="#000"
//   }
// })
// window.addEventListener("scroll",()=>{
//   if(window.pageYOffset>1400){
//     dot[3].style.color="#000"
//   }
// })
// window.addEventListener("scroll",()=>{
//   if(window.pageYOffset>1600){
//     dot[4].style.color="#000"
//   }
// })

// accprdian part 2


var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("visuale");
    var panel = this.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
}
// const Hideicons=document.querySelectorAll(".hideicons");
// const showicons=document.querySelectorAll(".icon");
// const accordions = document.querySelectorAll(".accordi");
// accordions.forEach(accor => {
//     const icons = accor.querySelector(".icon");
//     const answer = accor.querySelector(".answer");

//     icons.addEventListener("click", (e)=> {
//     e.preventDefault();
//         icons.classList.toggle("active");
//         answer.classList.toggle("active");
//     })

// }) 

// for(let i=0;i<showicons.length;i++){
//   showicons[i].addEventListener("click",()=>{
//     showicons[i].classList.toggle("see");
//     Hideicons[i].classList.toggle("prove")
//     console.log('hello')
//    })
// }
// for(let i=0;i<showicons.length;i++){
//   Hideicons[i].addEventListener("click",()=>{
//     showicons[i].classList.toggle("see");
//     Hideicons[i].classList.toggle("prove")
//     console.log('hey')
//    })
// }

// tab js
function openCity(evt, cityName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}


const opacity=document.querySelector("#opacity");
const footer1=document.querySelector(".footer-above-section");
const footer2=document.querySelector(".footer-section");
const topsection=document.querySelector(".top-section-remote");

function clickoff(){
  topsection.classList.remove("open-close");
  opacity.style.display="block";
  footer1.style.display="block";
  footer2.style.display="block";
}
function clickOnn(){
  topsection.classList.add("open-close");
  opacity.style.display="none";
  footer1.style.display="none";
  footer2.style.display="none";
}

const scrollOpen=document.querySelector(".bg-add-color");
const cross=document.querySelector(".cross-icon");

const showsort=document.querySelector(".show-sort");
cross.addEventListener("click",()=>{
  showsort.style.display="none";
  footer1.style.display="block";
  footer2.style.display="block";
  opacity.style.opacity="1";
  scrollOpen.style.opacity="1";
})



const clicksort=document.querySelector(".click-sort");
clicksort.addEventListener("click",()=>{
  showsort.style.display="block";
  opacity.style.opacity="0.1";
  footer1.style.display="none";
  footer2.style.display="none";
  scrollOpen.style.opacity="0";
})




// mobile view list-item design

const showProperties=document.querySelectorAll(".show-body");


const tab=document.querySelectorAll(".tab-btn");
for (let i in tab) {
tab[i].addEventListener("click",()=>{
   showProperties.forEach(visual=>{
    visual.style.display="none";
   })
    tab[i].style.color="rgb(45, 45, 45)";
    showProperties[i].style.display="block";
    
})
}





