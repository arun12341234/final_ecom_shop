



// login page
const Box1=document.querySelector(".box");
const Box2=document.querySelector(".box1");
const email=document.getElementById("E-mail");
const num=document.getElementById("Mobile-num")

//   
// }

email.addEventListener("click",()=>{
Box1.style.display="none";
Box2.style.display="block";
})
num.addEventListener("click",()=>{
    Box2.style.display="none";
    Box1.style.display="block";
    })

    // <!-- Accordions  -->

const first=document.querySelector("first");
first.addEventListener("click",()=>{
    visualViewport.style.display="block"
})
const QuesBtn=document.querySelectorAll(".questions");
const AnsBtn=document.querySelectorAll(".answer");


for(let i=0;i<QuesBtn.length;i++){
    QuesBtn[i].addEventListener("click",()=>{
            
            AnsBtn[i].style.height = "50px";
            })
}