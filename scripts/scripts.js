function hamburger_menu(icon_id, nav_id, class_name) {
    var icon_el = document.getElementById(icon_id);
    var nav_el = document.getElementById(nav_id);

    if (icon_el.classList.contains(class_name)) {
        icon_el.classList.remove(class_name)
        nav_el.classList.remove(class_name)
    } else {
        icon_el.classList.add(class_name)
        nav_el.classList.add(class_name)
    }
}