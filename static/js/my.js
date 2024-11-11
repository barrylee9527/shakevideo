var app = new Vue({
    el: '#app',
    data: {
        logo: '1.png',
        play_url: '',
        playbackRates: [0.5, 1, 1.5, 2],
        play_url2: "",
        autoplay: true,
    },
    mounted() {
        var elevideo = document.getElementById("video");
        myPlayer = videojs('video');
        //播放器初始音量
        myPlayer.volume(0.6);
        //播放器播放出错或者播放完成时触发
        var count_errors = 0;
        myPlayer.on('error', function () {
            console.log(count_errors);
            count_errors += 1;
            if (count_errors > 100) {
                alert("哇，你牛皮，视频可能被你刷完了，请重启！");
                //消息提示
                count_errors = 0;
                myPlayer.pause();
            } else {
                pywebview.api.next_one().then((data) => {
                    var data_video = {
                        src: data,
                        type: 'video/mp4'
                    };
                    myPlayer.src(data_video);
                    myPlayer.load(data_video);
                    var playPromise = myPlayer.play().type;
                    if (playPromise !== undefined) {
                        playPromise.then(() => {
                            myPlayer.play()
                        }).catch(() => {
                        })
                    }
                })
            }
        });
        elevideo.addEventListener('ended', function () {
            console.log(count_errors);
            count_errors += 1;
            if (count_errors > 100) {
                alert("哇，你牛皮，视频可能被你刷完了，请重启！");
                count_errors = 0;
                myPlayer.pause();
            } else {
                pywebview.api.next_one().then((data) => {
                    var data_video = {
                        src: data,
                        type: 'video/mp4'
                    };
                    myPlayer.src(data_video);
                    myPlayer.load(data_video);
                    var playPromise = myPlayer.play().type;
                    if (playPromise !== undefined) {
                        playPromise.then(() => {
                            myPlayer.play()
                        }).catch(() => {
                        })
                    }
                })
            }
        });
    },
    methods: {
        fresh() {
            var data_video1 = {
                src: this.play_url,
                type: 'video/mp4'
            };
            console.log(this.play_url);
            myPlayer.src(data_video1);
            myPlayer.load(data_video1);
            var playPromise = myPlayer.play().type;
            console.log(playPromise);
            if (playPromise !== undefined) {
                playPromise.then(() => {
                    myPlayer.play();
                }).catch(() => {
                })
            }
        }
    }
})
window.addEventListener('pywebviewready', function () {
    console.log('weview API初始化完成');
    pywebview.api.load_video().then(() => {
    })
})
//监听键盘右键事件，播放下一个视频
document.oncontextmenu = function (e) {
    e.preventDefault();
    pywebview.api.next_one().then((data) => {
        var data_video = {
            src: data,
            type: 'video/mp4'
        };
        myPlayer.src(data_video);
        myPlayer.load(data_video);
        var playPromise = myPlayer.play().type;
        if (playPromise !== undefined) {
            playPromise.then(() => {
                myPlayer.play()
            }).catch(() => {
            })
        }
    })
};