// ===================== LIKE BUTTON =====================

const likeButtons = document.querySelectorAll(".like");

likeButtons.forEach(button => {

    button.addEventListener("click", function () {

        if (button.innerHTML.includes("fa-regular")) {

            button.innerHTML =
                '<i class="fa-solid fa-heart"></i> Liked';

            button.style.color = "red";

        } else {

            button.innerHTML =
                '<i class="fa-regular fa-heart"></i> Like';

            button.style.color = "white";

        }

    });
});


// ===================== SAVE BUTTON =====================

const saveButtons = document.querySelectorAll(".save");

saveButtons.forEach(button => {

    button.addEventListener("click", function () {

        if (button.innerHTML.includes("fa-regular")) {

            button.innerHTML =
                '<i class="fa-solid fa-bookmark"></i> Saved';

            button.style.color = "#1877f2";

            alert("News Saved Successfully!");

        } else {

            button.innerHTML =
                '<i class="fa-regular fa-bookmark"></i> Save';

            button.style.color = "white";   // ✅ changed

        }

    });

});

    

// ===================== SEARCH =====================

const search = document.querySelector(".search-box input");

search.addEventListener("keyup", function () {

    let value = search.value.toLowerCase();

    let cards = document.querySelectorAll(".card");

    cards.forEach(function(card){

        let title = card.querySelector("h2").textContent.toLowerCase();

        if(title.includes(value)){

            card.style.display = "block";

        }

        else{

            card.style.display = "none";

        }

    });

});


// ===================== PROFILE DROPDOWN =====================

const profileIcon = document.querySelector(".profile-icon");
const profileDropdown = document.querySelector(".profile-dropdown");

profileIcon.addEventListener("click", function(event) {

    event.stopPropagation();

    profileDropdown.classList.toggle("show");

});
document.addEventListener("click", function(event) {

    if (!event.target.closest(".profile-menu")) {
        profileDropdown.classList.remove("show");
    }

});


// ===================== NOTIFICATION =====================

const bell = document.querySelector(".fa-bell");

bell.addEventListener("click", function(){

    alert("No New Notifications");

});


// ===================== MENU =====================

const menuItems = document.querySelectorAll(".left-sidebar li");

menuItems.forEach(function(item){

    item.addEventListener("click", function(){

        menuItems.forEach(i=>i.style.background="white");

        menuItems.forEach(i=>i.style.color="black");

        item.style.background="#1877f2";

        item.style.color="white";

    });

});


// ===================== COMMENT =====================

const commentButtons = document.querySelectorAll(".buttons button:nth-child(3)");

commentButtons.forEach(button=>{

    button.addEventListener("click",function(){

        let comment = prompt("Write your comment");

        if(comment){

            alert("Comment Added:\n\n"+comment);

        }

    });

});
