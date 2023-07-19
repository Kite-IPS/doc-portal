function addLockInfo(box){
    var form = document.getElementsByTagName('form')[0];
    var lock = document.getElementById("lock-box");

    if(!box.checked)
    {
        document.getElementById("lock-box").remove();
        console.log("Element removed");
    }
    else{
        var lock = document.createElement("input");
        lock.type = "hidden";
        lock.name = "lock";
        lock.value = "on";
        lock.id = "lock-box";
        form.appendChild(lock);
        console.log("element added");
    }
}