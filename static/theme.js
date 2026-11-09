(function () {
  var root = document.documentElement;
  var reduced = matchMedia("(prefers-reduced-motion: reduce)");

  // 見た目を変える時は View Transitions で前後をつなぐ
  function change(fn) {
    if (document.startViewTransition && !reduced.matches) document.startViewTransition(fn);
    else fn();
  }

  // 配色（ライト・ダーク）
  var button = document.querySelector(".theme-toggle");
  if (button) {
    var current = function () {
      var t = root.dataset.theme;
      if (t === "light" || t === "dark") return t;
      return matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    };
    var label = function () {
      var next = current() === "dark" ? "ライト" : "ダーク";
      button.setAttribute("aria-label", next + "表示に切り替える");
      button.title = next + "表示に切り替える";
    };
    button.hidden = false;
    label();
    button.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      change(function () {
        root.dataset.theme = next;
        label();
      });
      try { localStorage.setItem("theme", next); } catch (e) {}
    });
  }

  // 表示の設定（テーマ・印の色・等幅フォント）
  var prefs = document.getElementById("prefs");
  var opener = document.querySelector(".prefs-button");
  if (prefs && opener) {
    ["style", "accent", "font"].forEach(function (key) {
      var checked = prefs.querySelector('input[name="' + key + '"][value="' + root.getAttribute("data-" + key) + '"]');
      if (checked) checked.checked = true;
    });
    prefs.addEventListener("change", function (e) {
      var input = e.target;
      change(function () { root.setAttribute("data-" + input.name, input.value); });
      try { localStorage.setItem(input.name, input.value); } catch (e2) {}
    });
    opener.hidden = false;
  }
})();
