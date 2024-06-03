const header = document.querySelector("header");
window.addEventListener("scroll", function () {
  header.classList.toggle("sticky", window.scrollY > 200);
});

let menu = document.querySelector("#menu-icon");
let navlist = document.querySelector(".navlist");

menu.onclick = () => {
  menu.classList.toggle("bx-x");
  navlist.classList.toggle("open");
};

window.onscroll = () => {
  menu.classList.remove("bx-x");
  navlist.classList.remove("open");
};

// Add to cart
// function addToCart(productId) {
//   fetch("/add_to_cart", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ product_id: productId }),
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       const cartContainer = document.getElementById("cart-container");
//       const cartList = document.getElementById("cart");
//       cartList.innerHTML = "";
//       data.forEach((item) => {
//         const li = document.createElement("li");
//         li.textContent = `${item.name} - Rs.${item.price}`;
//         cartList.appendChild(li);
//       });
//       cartContainer.classList.remove("hidden");
//     })
//     .catch((error) => console.error("Error:", error));
// }
