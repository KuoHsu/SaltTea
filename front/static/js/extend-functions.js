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

function tdCreater(
  text,
  fontSize = "12px",
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

function createOperationTable(table, dataObj, isBranch = false) {
  $("#" + table).html("");

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
    (isBranch ? "臺科大分店營運概況表" : "總體營運概況表");

  var info =
    (isBranch ? "分店代碼：" + dataObj.branchId : "") +
    "報表期間：2019年" +
    dataObj.month +
    "月";

  $(trs[0]).append(tdCreater("鹽茶", "20px", "center", "none", 2));
  $(trs[0]).css("font-weight", "bolder");
  $(trs[1]).append(
    tdCreater(subtitle, "16px", "center", borderStyle["bolder"], 2)
  );
  $(trs[1]).css("font-weight", "bolder");

  $(trs[2]).append(tdCreater(info, "8px", "right", "none", 2));

  $(trs[3]).append(tdCreater("單位：新台幣元", "8px", "right", "none", 2));

  $(trs[4]).append(tdCreater("　", "8px", "center", "none", 2));

  $(trs[5]).append(tdCreater("項目", "14px", "center", borderStyle["normal"]));
  $(trs[5]).append(tdCreater("總額", "14px", "center", borderStyle["normal"]));
  $(trs[5]).css("font-weight", "bolder");

  $(trs[6]).append(tdCreater("銷貨收入", "12px", "center", "none"));
  $(trs[6]).append(tdCreater(priceFormat(rc[0]), "12px", "right", "none"));

  $(trs[7]).append(tdCreater("銷貨成本", "12px", "center", "none"));
  $(trs[7]).append(tdCreater(priceFormat(rc[1]), "12px", "right", "none"));

  $(trs[8]).append(tdCreater("薪資支出", "12px", "center", "none"));
  $(trs[8]).append(tdCreater(priceFormat(rc[2]), "12px", "right", "none"));

  $(trs[9]).append(tdCreater("水電瓦斯費", "12px", "center", "none"));
  $(trs[9]).append(tdCreater(priceFormat(rc[3]), "12px", "right", "none"));

  $(trs[10]).append(
    tdCreater("租金費用", "12px", "center", borderStyle["double"])
  );
  $(trs[10]).append(
    tdCreater(priceFormat(rc[4]), "12px", "right", borderStyle["double"])
  );

  $(trs[11]).append(tdCreater("總計", "14px", "center", "none"));
  $(trs[11]).append(tdCreater(priceFormat(total), "14px", "right", "none"));

  console.log(trs);

  $("#" + table).append(trs);
  $("#" + table).css("border", "dotted 2px #111");
  $("#" + table + " td").css("width", "5%");
  $("#" + table + " td").css("padding", "0 6px");
}

function createSalesTable(isBranch = false) {}
