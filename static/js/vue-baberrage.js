!function (e, t) {
    "object" == typeof exports && "undefined" != typeof module ? t(exports, require("timers")) : "function" == typeof define && define.amd ? define(["exports", "timers"], t) : t((e = e || self)["vue-baberrage"] = {}, e.timers)
}(this, (function (e, t) {
    "use strict";

    function n(e, t, n) {
        return t in e ? Object.defineProperty(e, t, {
            value: n,
            enumerable: !0,
            configurable: !0,
            writable: !0
        }) : e[t] = n, e
    }

    function i(e, t) {
        var n = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
            var i = Object.getOwnPropertySymbols(e);
            t && (i = i.filter((function (t) {
                return Object.getOwnPropertyDescriptor(e, t).enumerable
            }))), n.push.apply(n, i)
        }
        return n
    }

    function a(e) {
        return function (e) {
            if (Array.isArray(e)) {
                for (var t = 0, n = new Array(e.length); t < e.length; t++) n[t] = e[t];
                return n
            }
        }(e) || function (e) {
            if (Symbol.iterator in Object(e) || "[object Arguments]" === Object.prototype.toString.call(e)) return Array.from(e)
        }(e) || function () {
            throw new TypeError("Invalid attempt to spread non-iterable instance")
        }()
    }

    for (var r = function (e, t) {
        return e(t = {exports: {}}, t.exports), t.exports
    }((function (e) {
        var t = "undefined" != typeof crypto && crypto.getRandomValues && crypto.getRandomValues.bind(crypto) || "undefined" != typeof msCrypto && "function" == typeof window.msCrypto.getRandomValues && msCrypto.getRandomValues.bind(msCrypto);
        if (t) {
            var n = new Uint8Array(16);
            e.exports = function () {
                return t(n), n
            }
        } else {
            var i = new Array(16);
            e.exports = function () {
                for (var e, t = 0; t < 16; t++) 0 == (3 & t) && (e = 4294967296 * Math.random()), i[t] = e >>> ((3 & t) << 3) & 255;
                return i
            }
        }
    })), s = [], o = 0; o < 256; ++o) s[o] = (o + 256).toString(16).substr(1);
    var u = function (e, t) {
        var n = t || 0, i = s;
        return [i[e[n++]], i[e[n++]], i[e[n++]], i[e[n++]], "-", i[e[n++]], i[e[n++]], "-", i[e[n++]], i[e[n++]], "-", i[e[n++]], i[e[n++]], "-", i[e[n++]], i[e[n++]], i[e[n++]], i[e[n++]], i[e[n++]], i[e[n++]]].join("")
    };
    var l = function (e, t, n) {
        var i = t && n || 0;
        "string" == typeof e && (t = "binary" === e ? new Array(16) : null, e = null);
        var a = (e = e || {}).random || (e.rng || r)();
        if (a[6] = 15 & a[6] | 64, a[8] = 63 & a[8] | 128, t) for (var s = 0; s < 16; ++s) t[i + s] = a[s];
        return t || u(a)
    }, d = /[A-Z]/g, h = /^ms-/, m = {};

    function p(e) {
        return "-" + e.toLowerCase()
    }

    function c(e) {
        if (m.hasOwnProperty(e)) return m[e];
        var t = e.replace(d, p);
        return m[e] = h.test(t) ? "-" + t : t
    }

    var f = {
        name: "vue-baberrage-message", props: {
            item: {
                type: Object, default: function () {
                    return {}
                }
            }
        }, data: function () {
            return {isCustom: !1}
        }, mounted: function () {
            this.isCustom = !!this.$scopedSlots.default
        }
    };

    function b(e, t, n, i, a, r, s, o, u, l) {
        "boolean" != typeof s && (u = o, o = s, s = !1);
        const d = "function" == typeof n ? n.options : n;
        let h;
        if (e && e.render && (d.render = e.render, d.staticRenderFns = e.staticRenderFns, d._compiled = !0, a && (d.functional = !0)), i && (d._scopeId = i), r ? (h = function (e) {
            (e = e || this.$vnode && this.$vnode.ssrContext || this.parent && this.parent.$vnode && this.parent.$vnode.ssrContext) || "undefined" == typeof __VUE_SSR_CONTEXT__ || (e = __VUE_SSR_CONTEXT__), t && t.call(this, u(e)), e && e._registeredComponents && e._registeredComponents.add(r)
        }, d._ssrRegister = h) : t && (h = s ? function (e) {
            t.call(this, l(e, this.$root.$options.shadowRoot))
        } : function (e) {
            t.call(this, o(e))
        }), h) if (d.functional) {
            const e = d.render;
            d.render = function (t, n) {
                return h.call(n), e(t, n)
            }
        } else {
            const e = d.beforeCreate;
            d.beforeCreate = e ? [].concat(e, h) : [h]
        }
        return n
    }

    const g = "undefined" != typeof navigator && /msie [6-9]\\b/.test(navigator.userAgent.toLowerCase());

    function A(e) {
        return (e, t) => function (e, t) {
            const n = g ? t.media || "default" : e, i = y[n] || (y[n] = {ids: new Set, styles: []});
            if (!i.ids.has(e)) {
                i.ids.add(e);
                let n = t.source;
                if (t.map && (n += "\n/*# sourceURL=" + t.map.sources[0] + " */", n += "\n/*# sourceMappingURL=data:application/json;base64," + btoa(unescape(encodeURIComponent(JSON.stringify(t.map)))) + " */"), i.element || (i.element = document.createElement("style"), i.element.type = "text/css", t.media && i.element.setAttribute("media", t.media), void 0 === v && (v = document.head || document.getElementsByTagName("head")[0]), v.appendChild(i.element)), "styleSheet" in i.element) i.styles.push(n), i.element.styleSheet.cssText = i.styles.filter(Boolean).join("\n"); else {
                    const e = i.ids.size - 1, t = document.createTextNode(n), a = i.element.childNodes;
                    a[e] && i.element.removeChild(a[e]), a.length ? i.element.insertBefore(t, a[e]) : i.element.appendChild(t)
                }
            }
        }(e, t)
    }

    let v;
    const y = {};
    const x = f;
    var w = function () {
        var e = this, t = e.$createElement, n = e._self._c || t;
        return n("div", {
            staticClass: "baberrage-item",
            class: e.item.barrageStyle,
            style: e.item.style
        }, [e.isCustom ? [e._t("default")] : n("div", {staticClass: "normal"}, [n("div", {staticClass: "baberrage-avatar"}, [n("img", {attrs: {src: e.item.avatar}})]), e._v(" "), n("div", {staticClass: "baberrage-msg"}, [e._v(e._s(e.item.msg))])])], 2)
    };
    w._withStripped = !0;
    const C = b({render: w, staticRenderFns: []}, (function (e) {
        e && e("data-v-600778c7_0", {
            source: ".baberrage-item {\n  position: absolute;\n  width: auto;\n  display: block;\n  color: #000;\n  transform: translateX(500%);\n  padding: 5px 0 5px 0;\n  box-sizing: border-box;\n  text-align: left;\n  white-space: nowrap;\n}\n.baberrage-item .normal {\n  display: flex;\n  box-sizing: border-box;\n  padding: 5px;\n}\n.baberrage-item .normal .baberrage-avatar {\n  width: 30px;\n  height: 30px;\n  border-radius: 50px;\n  overflow: hidden;\n}\n.baberrage-item .normal .baberrage-avatar img {\n  width: 30px;\n}\n.baberrage-item .baberrage-msg {\n  line-height: 30px;\n  padding-left: 8px;\n  white-space: nowrap;\n}\n.baberrage-item .normal {\n  background: rgba(0, 0, 0, 0.7);\n  border-radius: 100px;\n  color: #FFF;\n}\n",
            map: {
                version: 3,
                sources: ["index.vue", "/Users/chenhao/Documents/work/vue-baberrage/src/lib/components/vue-baberrage-msg/index.vue"],
                names: [],
                mappings: "AAAA;EACE,kBAAkB;EAClB,WAAW;EACX,cAAc;EACd,WAAW;EACX,2BAA2B;EAC3B,oBAAoB;EACpB,sBAAsB;EACtB,gBAAgB;EAChB,mBAAmB;AACrB;AACA;EACE,aAAa;EACb,sBAAsB;EACtB,YAAY;AACd;AACA;EACE,WAAW;EACX,YAAY;EACZ,mBAAmB;EACnB,gBAAgB;AAClB;AACA;EACE,WAAW;AACb;AACA;EACE,iBAAiB;EACjB,iBAAiB;EACjB,mBAAmB;AACrB;AACA;EACE,8BAA8B;ECChC,oBAAA;EACA,WAAA;AACA",
                file: "index.vue",
                sourcesContent: [".baberrage-item {\n  position: absolute;\n  width: auto;\n  display: block;\n  color: #000;\n  transform: translateX(500%);\n  padding: 5px 0 5px 0;\n  box-sizing: border-box;\n  text-align: left;\n  white-space: nowrap;\n}\n.baberrage-item .normal {\n  display: flex;\n  box-sizing: border-box;\n  padding: 5px;\n}\n.baberrage-item .normal .baberrage-avatar {\n  width: 30px;\n  height: 30px;\n  border-radius: 50px;\n  overflow: hidden;\n}\n.baberrage-item .normal .baberrage-avatar img {\n  width: 30px;\n}\n.baberrage-item .baberrage-msg {\n  line-height: 30px;\n  padding-left: 8px;\n  white-space: nowrap;\n}\n.baberrage-item .normal {\n  background: rgba(0, 0, 0, 0.7);\n  border-radius: 100px;\n  color: #FFF;\n}\n", '<template>\n  <div class="baberrage-item" v-bind:class="item.barrageStyle" v-bind:style="item.style">\n    <template v-if="isCustom">\n      <slot></slot>\n    </template>\n    <div v-else class="normal">\n      <div class="baberrage-avatar"><img :src="item.avatar"></div>\n      <div class="baberrage-msg">{{ item.msg }}</div>\n    </div>\n  </div>\n</template>\n<script>\nexport default {\n  name: \'vue-baberrage-message\',\n  props: {\n    item: {\n      type: Object,\n      default () { return {} }\n    }\n  },\n  data () {\n    return {\n      isCustom: false // 弹幕格式是否是自定义\n    }\n  },\n  mounted () {\n    this.isCustom = !!this.$scopedSlots.default\n  }\n}\n<\/script>\n\n<style lang="less">\n.baberrage-item {\n  position: absolute;\n  width:auto;\n  display:block;\n  color:#000;\n  transform: translateX(500%);\n  padding:5px 0 5px 0;\n  box-sizing: border-box;\n  text-align:left;\n  white-space:nowrap;\n\n  .normal {\n    display: flex;\n    box-sizing: border-box;\n    padding: 5px;\n\n    .baberrage-avatar {\n      width:30px;\n      height:30px;\n      border-radius:50px;\n      overflow: hidden;\n\n      img {\n        width:30px;\n      }\n    }\n  }\n\n  .baberrage-msg{\n    line-height:30px;\n    padding-left:8px;\n    white-space:nowrap;\n  }\n}\n\n.baberrage-item .normal{\n  background:rgba(0,0,0,.7);\n  border-radius:100px;\n  color:#FFF;\n}\n</style>\n']
            },
            media: void 0
        })
    }), x, void 0, !1, void 0, !1, A, void 0, void 0);
    var B = {NORMAL: Symbol("NORMAL"), FROM_TOP: Symbol("FROM_TOP"), FROM_BOTTOM: Symbol("FROM_BOTTOM")};
    var E = require("to-px");
    window.requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame, window.cancelAnimationFrame = window.cancelAnimationFrame || window.mozCancelAnimationFrame || function (e) {
        clearTimeout(e)
    };
    const O = {
        name: "vue-baberrage",
        components: {VueBaberrageMsg: C},
        props: {
            isShow: {type: Boolean, default: !0},
            lanesCount: {type: Number, default: 0},
            barrageList: {
                type: Array, default: function () {
                    return []
                }
            },
            boxWidth: {type: Number, default: 0},
            boxHeight: {type: Number, default: 0},
            messageHeight: {type: Number, default: 40},
            messageGap: {type: Number, default: 5},
            loop: {type: Boolean, default: !1},
            maxWordCount: {type: Number, default: 20},
            throttleGap: {type: Number, default: 2e3},
            posRender: {type: Function}
        },
        data: function () {
            return {
                boxWidthVal: this.boxWidth,
                boxHeightVal: this.boxHeight,
                loopVal: this.loop,
                laneNum: 0,
                lanes: [],
                startTime: 0,
                frameId: null,
                readyId: 0,
                topQueue: [],
                bottomQueue: [],
                normalQueue: [],
                showInd: 0,
                indexShowQueue: [],
                taskQueue: [],
                taskIsRunning: !1,
                taskLastTime: null,
                isFixLanes: !1
            }
        },
        mounted: function () {
            0 === this.boxWidthVal && (this.boxWidthVal = this.$refs.stage.parentNode.offsetWidth), 0 === this.lanesCount ? this.setUpLane(this.boxHeightVal) : (this.setUpLane(this.lanesCount, !0), this.isFixLanes = !0), this.shuffle(), this.play()
        },
        watch: {
            barrageList: function (e) {
                this.insertToReadyShowQueue()
            }, boxHeight: function (e) {
                this.isFixLanes || this.setUpLane(e)
            }, lanes: function (e) {
                e > 0 && (this.setUpLane(e, !0), this.isFixLanes = !0)
            }
        },
        methods: {
            setUpLane: function (e) {
                var t = arguments.length > 1 && void 0 !== arguments[1] && arguments[1], n = this.laneNum >>> 0;
                if (t ? (this.laneNum = this.lanesCount, this.boxHeightVal = this.lanesCount * (this.messageHeight + this.messageGap)) : (0 === e && (e = 0 === (e = this.$refs.stage.parentNode.offsetHeight) ? window.innerHeight : e), this.boxHeightVal = e, this.laneNum = Math.floor(e / (this.messageHeight + 2 * this.messageGap))), n < this.laneNum) for (var i = n; i < this.laneNum; i++) this.lanes.push({
                    id: i,
                    laneQueue: []
                }); else this.lanes.splice(this.laneNum)
            }, shuffle: function () {
                var e = this.laneNum;
                this.indexShowQueue = Array.from({length: e}, (function (e, t) {
                    return t
                }))
            }, insertToReadyShowQueue: function () {
                var e = this;
                clearTimeout(this.readyId), this.readyId = t.setTimeout((function () {
                    for (var t = function () {
                        var t = e.barrageList.splice(0, e.laneNum);
                        e.addTask((function () {
                            e.normalQueue = [].concat(a(e.normalQueue), a(t))
                        }))
                    }; e.barrageList.length > 0;) t();
                    e.updateBarrageDate()
                }), 300)
            }, updateBarrageDate: function (e) {
                null == this.startTime && (this.startTime = e), void 0 !== e && this.move(e), this.normalQueue.length > 0 || this.topQueue.length > 0 || this.bottomQueue.length > 0 ? this.play() : (this.$emit("barrage-list-empty"), this.frameId = null)
            }, play: function () {
                this.frameId = requestAnimationFrame(this.updateBarrageDate)
            }, pause: function () {
                cancelAnimationFrame(this.frameId)
            }, replay: function () {
                this.normalQueue.forEach((function (e) {
                    e.startTime = null
                })), this.play()
            }, move: function (e) {
                var t = this;
                this.normalQueue.forEach((function (n, i) {
                    if (n.startTime) {
                        if (n.type === B.NORMAL && (t.normalMove(n, e), n.left + n.width < 0)) {
                            if (!t.lanes[n.laneId]) return;
                            var a = t.lanes[n.laneId].laneQueue.findIndex((function (e) {
                                return e.runtimeId === n.runtimeId
                            }));
                            t.lanes[n.laneId].laneQueue.splice(a, 1), t.loopVal ? t.itemReset(n, e) : t.normalQueue.splice(i, 1)
                        }
                    } else {
                        if (n.type === B.FROM_TOP) {
                            if ("top" !== n.position && "bottom" !== n.position) throw new Error("Position only between top and bottom when the type equal 1");
                            t.fixMove(n, e), t.normalQueue.splice(i, 1)
                        }
                        t.itemReset(n, e)
                    }
                })), this.queueRefresh(e)
            }, normalMove: function (e, t) {
                var n = t - e.currentTime;
                e.currentTime = t;
                var i = e.speed * n;
                i <= 0 || isNaN(i) || (e.left -= i, this.moveTo(e, {x: e.left, y: e.top < 0 ? 0 : e.top}))
            }, fixMove: function (e, t) {
                this[e.position + "Queue"].includes(e) || this[e.position + "Queue"].push(e)
            }, queueRefresh: function (e) {
                var t = this;
                this.topQueue.forEach((function (n) {
                    n.startTime + 1e3 * n.time <= e && t.topQueue.shift()
                })), this.bottomQueue.forEach((function (n) {
                    n.startTime + 1e3 * n.time <= e && t.bottomQueue.shift()
                }))
            }, selectPos: function () {
                return this.posRender ? this.posRender(this.lanes) : (this.showInd + 1 > this.laneNum && (this.showInd = 0), this.showInd++)
            }, isWaiting: function (e) {
                return e.left > this.boxWidthVal
            }, itemReset: function (e, t) {
                var n = this;
                if (e.runtimeId = l(), e.msg = e.data && e.data.msg || e.msg, e.type = e.type || B.NORMAL, e.position = e.position || "top", e.barrageStyle = e.barrageStyle || "normal", e.startTime = t, e.currentTime = t, e.speed = this.boxWidthVal / (1e3 * e.time), e.cssStyle = {}, Object.keys(e.style || {}).forEach((function (t) {
                    e.cssStyle[c(t)] = n.isNumber(e.style[t]) ? e.style[t] + "px" : e.style[t]
                })), e.width = this.strlen(e.msg) * this.toPxiel(e.cssStyle["font-size"] || "9px") * .6 + (e.extraWidth || 0) + function (e) {
                    if (!e) return 0;
                    var t = {}, n = 0;
                    return Object.keys(e || {}).forEach((function (i) {
                        switch (t[c(i)] = isNaN(e[i]) ? e[i] : e[i] + "px", c(i)) {
                            case"padding":
                                var a = e[i].split(" ");
                                4 === a.length ? n += +a[1].replace("px", "") + +a[3].replace("px", "") : 2 === a.length ? n += 2 * +a[1].replace("px", "") : n += 2 * +a[0].replace("px", "");
                                break;
                            case"padding-left":
                            case"padding-right":
                                n += +e[i].replace("px", "")
                        }
                    })), n
                }(e.cssStyle), e.type === B.NORMAL) {
                    var i = this.selectPos();
                    e.laneId = i;
                    var a = this.boxWidthVal;
                    if (this.lanes[i].laneQueue.length > 0) {
                        var r = this.lanes[i].laneQueue[this.lanes[i].laneQueue.length - 1];
                        r.left > this.boxWidthVal || r.left > this.boxWidthVal - r.width ? a = r.width + r.left : a += r.width
                    }
                    this.lanes[i].laneQueue.push(e), e.top = this.indexShowQueue[i] * (this.messageHeight + this.messageGap), e.left = a
                } else e.left = (this.boxWidthVal - e.width) / 2, "top" === e.position ? e.top = (this[e.position + "Queue"].length - 1) * this.messageHeight + 2 * this.messageGap : e.top = this.boxHeightVal - (this[e.position + "Queue"].length * this.messageHeight + 100);
                this.moveTo(e, {x: e.left, y: e.top < 0 ? 0 : e.top})
            }, toPxiel: function (e) {
                return this.isNumber(e) ? E(e + "px") : E(e)
            }, moveTo: function (e, t) {
                t.x, t.y;
                this.$set(e, "style", function (e) {
                    for (var t = 1; t < arguments.length; t++) {
                        var a = null != arguments[t] ? arguments[t] : {};
                        t % 2 ? i(Object(a), !0).forEach((function (t) {
                            n(e, t, a[t])
                        })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(a)) : i(Object(a)).forEach((function (t) {
                            Object.defineProperty(e, t, Object.getOwnPropertyDescriptor(a, t))
                        }))
                    }
                    return e
                }({}, e.cssStyle, {transform: "translate3d(" + e.left + "px," + e.top + "px,0)"}))
            }, addTask: function (e) {
                this.taskQueue.push(e), this.taskQueue.length > 0 && !this.taskIsRunning && (this.taskIsRunning = !0, window.requestAnimationFrame(this.runTask))
            }, runTask: function (e) {
                if (!this.taskLastTime || e - this.taskLastTime >= this.throttleGap) {
                    var t = this.taskQueue.shift();
                    this.taskLastTime = e, t()
                }
                this.taskQueue.length > 0 ? window.requestAnimationFrame(this.runTask) : this.taskIsRunning = !1
            }, strlen: function (e) {
                var t = 0;
                for (var n in e) e.charCodeAt(n) > 127 || 94 === e.charCodeAt(n) ? t += 2 : t++;
                return t
            }, isNumber: function (e) {
                return !isNaN(e)
            }
        }
    };
    var T = function () {
        var e = this, t = e.$createElement, n = e._self._c || t;
        return n("div", {
            directives: [{name: "show", rawName: "v-show", value: e.isShow, expression: "isShow"}],
            ref: "stage",
            staticClass: "baberrage-stage",
            style: {width: e.boxWidthVal + "px"}
        }, [n("div", {staticClass: "baberrage-top"}, e._l(e.topQueue, (function (e) {
            return n("VueBaberrageMsg", {key: e.id, staticClass: "baberrage-item", attrs: {item: e}})
        })), 1), e._v(" "), e._l(e.lanes, (function (t) {
            return n("div", {key: t.id, staticClass: "baberrage-lane"}, e._l(t.laneQueue, (function (t) {
                return n("VueBaberrageMsg", {
                    key: t.runtimeId,
                    staticClass: "baberrage-item",
                    attrs: {item: t}
                }, [e._t("default", null, {item: t})], 2)
            })), 1)
        })), e._v(" "), n("div", {staticClass: "baberrage-bottom"}, e._l(e.bottomQueue, (function (e) {
            return n("VueBaberrageMsg", {key: e.id, staticClass: "baberrage-item", attrs: {item: e}})
        })), 1)], 2)
    };
    T._withStripped = !0;
    const _ = b({render: T, staticRenderFns: []}, (function (e) {
        e && e("data-v-71e78858_0", {
            source: ".baberrage-stage {\n  position: absolute;\n  width: 100%;\n  height: 100%;\n  overflow: hidden;\n}\n",
            map: {
                version: 3,
                sources: ["vue-baberrage.vue"],
                names: [],
                mappings: "AAAA;EACE,kBAAkB;EAClB,WAAW;EACX,YAAY;EACZ,gBAAgB;AAClB",
                file: "vue-baberrage.vue",
                sourcesContent: [".baberrage-stage {\n  position: absolute;\n  width: 100%;\n  height: 100%;\n  overflow: hidden;\n}\n"]
            },
            media: void 0
        })
    }), O, void 0, !1, void 0, !1, A, void 0, void 0);
    _.install = function (e, t) {
        e.component(_.name, _)
    }, "undefined" != typeof window && window.Vue && window.Vue.use(_), e.MESSAGE_TYPE = B, e.vueBaberrage = _, Object.defineProperty(e, "__esModule", {value: !0})
}));