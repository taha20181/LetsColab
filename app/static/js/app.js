flag = 0;
$(".like-btn").click( function() {
	if (flag == 0) {
	    $(this).css('color', 'blue');
	    flag = 1;
        var likes = document.getElementsByClassName('likes-count').textContent;
        console.log(parseInt(likes));
      likes_ = parseInt(likes);
      likes_ = likes_ + 1;
      document.getElementsByClassName('likes-count').innerHTML = likes_;
	  } else {
  	$(this).css('color', 'black');
  	flag = 0;
    var likes = document.getElementsByClassName('likes-count').innerHTML;
      likes_ = parseInt(likes);
      likes_ = likes_ - 1;
      document.getElementsByClassName('likes-count').innerHTML = likes_;
  }
});