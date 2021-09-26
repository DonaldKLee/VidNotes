function copy_note_link() {
    link = document.getElementById("note_link");
    link.select();
    link.setSelectionRange(0, 100)
    document.execCommand("copy");
}


function swap() {
    video = document.getElementById("youtube_video_container");
    form = document.getElementById("left_container");
    link = document.getElementById("link");
    swap_button = document.getElementById("swap_button");
    
    document.getElementById("swap_icon").style.animation = "swap_spin 0.3s 1";

    if (swap_button.name  == "swap") { // Swap
        video.style.float = "left";
        video.style.right = "0%";
        video.style.left = "5%";

        form.style.left = "52.5%";
        link.style.left = "52.5%";
        swap_button.name = "Unswap";
    }
    else { // Unswap
        video.style.float = "right";
        video.style.left = "auto";
        video.style.right = "5%";

        form.style.left = "auto";
        link.style.left = "auto";
        
        swap_button.name = "swap";
    }

    setTimeout(() => { document.getElementById("swap_icon").style.animation = "none"; }, 300);

}