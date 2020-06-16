// ==UserScript==
// @name         DouYu
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://www.douyu.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    setTimeout(function(){
        document.getElementById('js-player-barrage').setAttribute('style','top: 40px;');
        var sty = document.createElement('style');
        sty.type='text/css';
        sty.innerHTML="#js-barrage-container li div a{display:none!important;}span.Barrage-icon.Barrage-noble{display:none!important;}.shark-webp .FansMedal.level-0,.shark-webp .FansMedal.level-1,.shark-webp .FansMedal.level-2,.shark-webp .FansMedal.level-3,.shark-webp .FansMedal.level-4,.shark-webp .FansMedal.level-5,.shark-webp .FansMedal.level-6,.shark-webp .FansMedal.level-7,.shark-webp .FansMedal.level-8,.shark-webp .FansMedal.level-9,.shark-webp .FansMedal.level-10,.shark-webp .FansMedal.level-11,.shark-webp .FansMedal.level-12,.shark-webp .FansMedal.level-13,.shark-webp .FansMedal.level-14,.shark-webp .FansMedal.level-15,.shark-webp .FansMedal.level-16,.shark-webp .FansMedal.level-17,.shark-webp .FansMedal.level-18,.shark-webp .FansMedal.level-19,.shark-webp .FansMedal.level-20,.shark-webp .FansMedal.level-21,.shark-webp .FansMedal.level-22,.shark-webp .FansMedal.level-23,.shark-webp .FansMedal.level-24,.shark-webp .FansMedal.level-25,.shark-webp .FansMedal.level-26,.shark-webp .FansMedal.level-27,.shark-webp .FansMedal.level-28,.shark-webp .FansMedal.level-29,.shark-webp .FansMedal.level-30{display:none!important;}.shark-webp .RoomLevel--10,.shark-webp .RoomLevel--11,.shark-webp .RoomLevel--12,.shark-webp .RoomLevel--13,.shark-webp .RoomLevel--14,.shark-webp .RoomLevel--15,.shark-webp .RoomLevel--16,.shark-webp .RoomLevel--17,.shark-webp .RoomLevel--18{display:none!important;}.Motor{display:none!important;}.shark-webp .Barrage-icon--roomAdmin{display:none!important;}.FansMedal.is-made{display:none!important;}#js-room-activity{display:none!important;}#js-bottom{display:none!important;}.layout-Player-rank{display:none!important;}.layout-Player-rankAll{display:none!important;}#js-player-toolbar .PlayerToolbar{display:none!important;}.layout-Player-effect{display:none!important;}.layout-Player-barrage{top:40px!important;}div[class^='closeBg']{display:none!important;}"
        document.head.appendChild(sty)
    }, 3000);
})();
