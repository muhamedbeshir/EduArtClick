// $(".list-v-steps li").click(function(){
//     $(".list-v-steps li").removeClass("active");
//     $(this).addClass("active");
// });
// $(".list-v-steps li a").click(function(){
//     $('.list-v-steps li a').removeClass("active");
//     $('.list-v-steps li').removeClass("active");
//     $(this).parent().addClass("active");
//     $(this).addClass("active");
// });

// $('.btnNext').click(function(){
//     $('.list-v-steps li').find('.active').removeClass("active");
//     $('.list-v-steps > .active').next('li').find('a').trigger('click').addClass("active");
//     $(this).removeClass("active");
// });

// $('.btnPrevious').click(function(){
//     $('.list-v-steps li').find('.active').removeClass("active");
//     $('.list-v-steps > .active').prev('li').find('a').trigger('click').addClass("active");
//     $(this).removeClass("active");
// });

$('.btnNext').click(function(){
    $('.list-v-steps li').find('.active').removeClass("active");
    $('.list-v-steps > .active').next('li').addClass('active').find('a').trigger('click').addClass("active");
    $('.list-v-steps > .active').prev('li').removeClass('active');
    $(this).removeClass("active");
});

$('.btnPrevious').click(function(){
    $('.list-v-steps li').find('.active').removeClass("active");
    $('.list-v-steps > .active').prev('li').addClass("active").find('a').trigger('click').addClass("active");
    $('.list-v-steps > .active').next('li').removeClass('active');
    $(this).removeClass("active");
});