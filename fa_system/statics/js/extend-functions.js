var username = "";
const borderStyle = {
  bolder: "solid 4px #000",
  normal: "solid 1px #000",
  double: "double 3px #000"
};
function setMessage(message) {
  $("#message").text(message);
}
function showMessage() {
  $("#messageAlter").css("transform", "scale(1)");
}

function closeMessage() {
  $("#messageAlter").css("transform", "scale(0)");
}

function stringCopy(string, times) {
  s = "";
  for (var t = 1; t <= times; t++) s += string;
  return s;
}

function priceFormat(price) {
  var formatter = numeral(price);
  return formatter.format("($  0,0)");
}

function numberFormat(number) {
  var formatter = numeral(number);
  return formatter.format("0,0");
}

function fontBolder(tableId, rowIndex) {
  $("#" + tableId + " tr")[rowIndex].style.fontWeight = "bolder";
}

function tdCreater(
  text,
  fontSize = "20px",
  textAlign = "center",
  borderBottom = "None",
  colSpan = 1
) {
  td = $("<td/>");
  td.css("font-size", fontSize);
  td.css("text-align", textAlign);
  td.css("border-bottom", borderBottom);
  td.attr("colspan", colSpan);
  td.html(text);
  return td;
}

function branchName(branchId) {
  return " 臺北區" + (Number(branchId) - 20000) + "號分店";
}

function createOperationTable(table, dataObj, isBranch = false) {
  var __table = "#" + table;
  $(__table).html("");

  var trString = stringCopy("<tr/>", 12);
  var trs = $(trString);

  var rc = [
    dataObj.sales,
    dataObj.costOfSales,
    dataObj.salary,
    dataObj.electric,
    dataObj.rent
  ];

  var total = rc[0];
  for (var i = 1; i <= 4; i++) total -= rc[i];

  var subtitle =
    "2019年" +
    dataObj.month +
    "月" +
    (isBranch ? branchName(dataObj.branchId) + "銷售詳情表" : "總體營運概況表");

  var info =
    (isBranch ? "分店代碼：" + dataObj.branchId : "") +
    "　報表期間：2019年" +
    dataObj.month +
    "月";

  $(trs[0]).append(tdCreater("鹽茶", "32px", "center", "none", 2));
  $(trs[0]).css("font-weight", "bolder");
  $(trs[1]).append(
    tdCreater(subtitle, "28px", "center", borderStyle.bolder, 2)
  );
  $(trs[1]).css("font-weight", "bolder");

  $(trs[2]).append(tdCreater(info, "14px", "right", "none", 2));

  $(trs[3]).append(tdCreater("單位：新台幣元", "14px", "right", "none", 2));

  $(trs[4]).append(tdCreater("　", "16px", "center", "none", 2));

  $(trs[5]).append(tdCreater("項目", "24px", "center", borderStyle.normal));
  $(trs[5]).append(tdCreater("總額", "24px", "center", borderStyle.normal));
  $(trs[5]).css("font-weight", "bolder");

  $(trs[6]).append(tdCreater("銷貨收入", "20px", "center", "none"));
  $(trs[6]).append(tdCreater(priceFormat(rc[0]), "20px", "right", "none"));

  $(trs[7]).append(tdCreater("銷貨成本", "20px", "center", "none"));
  $(trs[7]).append(tdCreater(priceFormat(rc[1]), "20px", "right", "none"));

  $(trs[8]).append(tdCreater("薪資支出", "20px", "center", "none"));
  $(trs[8]).append(tdCreater(priceFormat(rc[2]), "20px", "right", "none"));

  $(trs[9]).append(tdCreater("水電瓦斯費", "20px", "center", "none"));
  $(trs[9]).append(tdCreater(priceFormat(rc[3]), "20px", "right", "none"));

  $(trs[10]).append(
    tdCreater("租金費用", "20px", "center", borderStyle.double)
  );
  $(trs[10]).append(
    tdCreater(priceFormat(rc[4]), "20px", "right", borderStyle.double)
  );

  $(trs[11]).append(tdCreater("總計", "24px", "center", "none"));
  $(trs[11]).append(tdCreater(priceFormat(total), "24px", "right", "none"));

  $(__table).append(trs);
  $(__table).css("border", "dotted 2px #111");
  $(__table + " td").css("width", "300px");
  $(__table + " td").css("padding", "0 6px");
  fontBolder(table, 0);
  fontBolder(table, 1);
  fontBolder(table, 11);
}

function createSalesTable(table, dataObj, isBranch = false) {
  __table = "#" + table;
  $(__table).html("");
  var trString = stringCopy("<tr/>", 5);
  var trs_title = $(trString);

  var subtitle =
    "2019年" +
    dataObj.month +
    "月" +
    (isBranch ? branchName(dataObj.branchId) + "銷售詳情表" : "總體銷售詳情表");

  var info =
    (isBranch ? "分店代碼：" + dataObj.branchId : "") +
    "　報表期間：2019年" +
    dataObj.month +
    "月";

  /*Table Header*/
  $(trs_title[0]).append(tdCreater("鹽茶", "32px", "center", "none", 6));
  $(trs_title[0]).css("font-weight", "bolder");
  $(trs_title[1]).append(
    tdCreater(subtitle, "28px", "center", borderStyle.bolder, 6)
  );
  $(trs_title[1]).css("font-weight", "bolder");

  $(trs_title[2]).append(tdCreater(info, "14px", "right", "none", 6));

  $(trs_title[3]).append(
    tdCreater("單位：新台幣元", "14px", "right", "none", 6)
  );

  $(trs_title[4]).append(tdCreater("　", "16px", "center", "none", 6));
  $(__table).append(trs_title);
  $(__table).append(getSalesTableItemTitle);
  /*Table Header end*/

  /*itemInfos*/

  var groups = dataObj.groups;
  var totalQuantity = 0;
  var totalSales = 0;
  for (var groupId in groups) {
    data = getSalesTableGroupInfo(groupId, groups[groupId]);
    rows = data.rows;
    for (var index in rows) $(__table).append(rows[index]);
    totalQuantity += data.quantity;
    totalSales += data.sales;
  }
  /*itemInfos end*/

  /*total*/
  totalTr = $("<tr/>");

  $(totalTr).append(tdCreater("總計", "24px", "right", "none", 4));
  $(totalTr).append(
    tdCreater(numberFormat(totalQuantity), "24px", "right", "none")
  );
  $(totalTr).append(
    tdCreater(priceFormat(totalSales), "24px", "right", "none")
  );

  $(__table).append(totalTr);

  $("#queryReport tr")
    .last()
    .css("border-top", borderStyle.double);
  /*total end */

  $(__table + " td").css("width", "5%");
  rowCount = $(__table + " tr").length;
  fontBolder(table, 0);
  fontBolder(table, 1);
  fontBolder(table, 5);
  fontBolder(table, rowCount - 1);
}

function getSalesTableItemTitle() {
  tr = $("<tr/>");
  title = ["商品編號", "商品名稱", "商品群組", "單價", "銷售量", "銷售額"];
  for (var i = 0; i < 6; i++) {
    $(tr).append(tdCreater(title[i], "20px", "center"));
  }
  $(tr).css("border-bottom", borderStyle.normal);
  return tr;
}

function getSalesTableGroupInfo(groupId, items) {
  var data = { quantity: 0, sales: 0, rows: [] };
  var totalQuantity = 0;
  var totalSales = 0;
  var rows = data.rows;
  var fontSize = "20px";
  var amountOfItem = items.length;
  var count = 1;

  /*itemInfo*/
  for (var key in items) {
    item = items[key];
    tr = $("<tr/>");
    /*Id, name, group*/
    $(tr).append(tdCreater(item.itemid, fontSize, "cneter", "none"));
    $(tr).append(tdCreater(item.itemName, fontSize, "cneter", "none"));
    $(tr).append(tdCreater(groupId, fontSize, "cneter", "none"));

    /*price, quantity, sales*/
    var sales = item.price * item.quantity;
    tdPrice = tdCreater(priceFormat(item.price), fontSize, "right", "none");
    tdQuantity = tdCreater(
      numberFormat(item.quantity),
      fontSize,
      "right",
      "none"
    );
    tdSales = tdCreater(priceFormat(sales), fontSize, "right", "none");
    $(tr).append(tdPrice);
    $(tr).append(tdQuantity);
    $(tr).append(tdSales);

    /*last row should draw the double-line under the data.*/
    if (count == amountOfItem) {
      $(tdQuantity).css("border-bottom", borderStyle.double);
      $(tdSales).css("border-bottom", borderStyle.double);
    }

    totalQuantity += item.quantity;
    totalSales += sales;
    rows.push(tr);
    count++;
  }
  /*itemInfo end*/

  /*amount*/
  totalTr = $("<tr/>");
  $(totalTr).append(tdCreater("小計", fontSize, "right", "none", 4));
  $(totalTr).append(
    tdCreater(numberFormat(totalQuantity), fontSize, "right", "none")
  );
  $(totalTr).append(
    tdCreater(priceFormat(totalSales), fontSize, "right", "none")
  );
  rows.push(totalTr);
  emptyTr = $("<tr/>");
  $(emptyTr).append(tdCreater("　", fontSize, "right", "none", 6));
  rows.push(emptyTr);
  /*amount end*/
  data.quantity = totalQuantity;
  data.sales = totalSales;

  return data;
}

function drawArray(id, arr, color) {
  /*Edit by 李丞彥*/
  var c = document.getElementById(id);
  var ctx = c.getContext("2d");
  var len = arr.length;
  var space = c.width / (len + 1);

  for (var i = 0; i < len; i++) {
    // ctx.moveTo((i+1)*space, arr[i]);
    ctx.beginPath();
    ctx.arc((i + 1) * space, c.height - arr[i], 1, 0, 2 * Math.PI);
    if (color == "r") {
      ctx.strokeStyle = "red";
    } else {
      ctx.strokeStyle = "black";
    }
    ctx.stroke();
    //ctx.closePath();
  }
  ctx.beginPath();
  ctx.moveTo(space, c.height - arr[0]);
  for (var j = 1; j < len; j++) {
    console.log(c.height - arr[j]);
    ctx.lineTo((j + 1) * space, c.height - arr[j]);
  }
  ctx.stroke();
}
