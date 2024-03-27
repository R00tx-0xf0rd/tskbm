function redirect() {
  console.log("clicked");
  window.location = "/";
}

function doFunction() {
  setTimeout(redirect, 5000);
}

function process() {
  if (confirm("Хотите добавить срок поверки ?")) {
    // Save it!
    console.log("Thing was saved to the database.");
  } else {
    // Do nothing!
    console.log("Thing was not saved to the database.");
  }
}

async function get_result(url) {
  fetch(url)
    .then((resp) => {
      if (!resp.ok) {
        throw Error(`is not ok: ` + resp.status);
      }
      return resp.json();
    })
    .catch((err) => {
      console.warn(err);
    });
}

async function get_periods() {
  let tabnum = document.querySelector("#checkout_tn").value;

  console.log(tabnum);
  element = document.querySelector(".answer");
  let url = "/users/" + tabnum + "/";

  let result = await fetch(url).then((resp) => resp.json());

  if (!result) {
    element.innerText = "Не найдено";
  } else {
    console.log(result);
    element.innerText = result.lname;
  }

  // let user = NaN;
  // if (response.ok) {
  //   console.log("ok");
  //   // если HTTP-статус в диапазоне 200-299
  //   // получаем тело ответа (см. про этот метод ниже)
  //   user = await response.json();
  // }
  // if (user != isNaN) {

  // }

  // console.log(user);
  // document.location = "/";
}
