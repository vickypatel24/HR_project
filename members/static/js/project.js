var table = document.querySelector(".table");
var row1 = document.querySelector(".tbody");
var num = 0;
var stnum = 0;

function row() {
  num++;
  stnum++;
  row1.insertAdjacentHTML(
    "beforeend",
    `<tr class='tablerow${num}'><td class='stnum'>${num}</td><td>vitrag</td><td><input class='math${num}' onchange='total(${num})'value='0'type='number' ></td><td ><input class='science${num}' value='0' type='number' onchange='total(${num})'></td><td ><input value='0' class='sst${num}' type='number'onchange='total(${num})'></td><td class='total${num} allTotal'></td><td class='pr${num}'></td><td><button class='btn btn-outline btn-danger deletrow${num}' onclick=remove(${num})>delete</button></td></tr>`
  );
}
function total(num) {
  var a = document.querySelector(`.math${num}`).value;
  var b = document.querySelector(`.science${num}`).value;
  var c = document.querySelector(`.sst${num}`).value;
  var d = parseFloat(a) + parseFloat(b) + parseFloat(c);
  document.querySelector(`.total${num}`).innerHTML = d;
  var pr = (d / 300) * 100;
  document.querySelector(`.pr${num}`).innerHTML = pr + "%";
  xyz();
}

function xyz() {
  document.querySelector(".totalstudent").innerHTML = stnum;
  var totalnum = document.querySelectorAll(".allTotal");
  let hmarks = [];
  totalnum.forEach((element) => {
    hmarks.push(Number(element.innerHTML));
  });
  var h = hmarks.sort(function (a, b) {
    return b - a;
  });
  var length = hmarks.length;
  document.querySelector(".high").innerHTML = hmarks[0];
  document.querySelector(".low").innerHTML = hmarks[length - 1];

  let avgsum = hmarks.reduce(myFunction);
  let aa = avgsum / stnum;
  document.querySelector(".avarage").innerHTML = aa;
  function myFunction(total, value) {
    return total + value;
  }
}

function remove(num) {
  stnum--;
  var tbrow = document.querySelector(`.tablerow${num}`);
  tbrow.remove();
  xyz();
}
