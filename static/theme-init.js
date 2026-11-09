(function () {
  var root = document.documentElement;
  try {
    var t = localStorage.getItem("theme");
    if (t === "light" || t === "dark") root.dataset.theme = t;
    // 表示の設定。一覧（data-styles など）にない古い値は使わない
    ["style", "accent", "font"].forEach(function (key) {
      var v = localStorage.getItem(key);
      var list = (root.getAttribute("data-" + key + "s") || "").split(" ");
      if (v && list.indexOf(v) !== -1) root.setAttribute("data-" + key, v);
    });
  } catch (e) {}
})();
