import{d as N,m as a,r as M,n as pe,p as C,q as Me,t as J,s as g,x as Ro,y as m,z as Ho,A,C as p,D as ko,T as Ao,N as Ze,E as de,F as ce,G as oe,H as Po,I as Oo,J as Ae,K as Lo,V as Je,L as te,M as q,O as W,P as re,Q as Pe,R as Ie,S as _o,U as Qe,W as eo,X as Ee,Y as To,Z as $o,_ as No,$ as Bo,a0 as ee,a1 as Mo,a2 as Eo,a3 as oo,a4 as Fo,a5 as ge,a6 as to,a7 as ro,a8 as no,a9 as G,aa as ae,ab as jo,ac as le,ad as Oe,ae as Se,af as lo,ag as be,ah as Vo,ai as Ko,o as j,c as Y,a as O,u as Do,aj as Z,w as K,g as $,i as Uo,h as Yo,ak as Wo,e as V,k as xe,al as Ce,B as he,am as Go,an as qo,ao as Xo,l as Fe,ap as ye}from"./index-CRYXIsvh.js";import{_ as Zo}from"./_plugin-vue_export-helper-DlAUqK2U.js";import{d as Jo,C as Qo,N as io}from"./Dropdown-FEeEDxR3.js";import{f as we}from"./format-length-B-p6aW7q.js";import{a as Re,u as et}from"./use-message-BppchCHs.js";import{t as ot,N as tt}from"./Tooltip-LbMNDyVw.js";import{g as rt,V as nt,c as ze}from"./Popover-CB8JeE3n.js";import{t as lt,u as it,N as at}from"./Space-DOsY5xaG.js";import{N as se}from"./Icon-B4ktjwSh.js";import{i as st,o as ct}from"./utils-D4cwJIpN.js";import{U as je}from"./UserOutlined-C0JAUwKe.js";import{S as Ve,F as Ke,T as dt}from"./TagsOutlined-DrFMOewj.js";import{T as ut}from"./ToolOutlined-BjV-4HZ5.js";import{C as De}from"./CloudDownloadOutlined-CjoOS0pt.js";import"./create-ref-setter-C4J8sofl.js";const vt=N({name:"ChevronDownFilled",render(){return a("svg",{viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg"},a("path",{d:"M3.20041 5.73966C3.48226 5.43613 3.95681 5.41856 4.26034 5.70041L8 9.22652L11.7397 5.70041C12.0432 5.41856 12.5177 5.43613 12.7996 5.73966C13.0815 6.0432 13.0639 6.51775 12.7603 6.7996L8.51034 10.7996C8.22258 11.0668 7.77743 11.0668 7.48967 10.7996L3.23966 6.7996C2.93613 6.51775 2.91856 6.0432 3.20041 5.73966Z",fill:"currentColor"}))}}),Ue=N({name:"SlotMachineNumber",props:{clsPrefix:{type:String,required:!0},value:{type:[Number,String],required:!0},oldOriginalNumber:{type:Number,default:void 0},newOriginalNumber:{type:Number,default:void 0}},setup(e){const t=M(null),o=M(e.value),n=M(e.value),l=M("up"),r=M(!1),s=C(()=>r.value?`${e.clsPrefix}-base-slot-machine-current-number--${l.value}-scroll`:null),u=C(()=>r.value?`${e.clsPrefix}-base-slot-machine-old-number--${l.value}-scroll`:null);pe(J(e,"value"),(b,z)=>{o.value=z,n.value=b,Me(d)});function d(){const b=e.newOriginalNumber,z=e.oldOriginalNumber;z===void 0||b===void 0||(b>z?v("up"):z>b&&v("down"))}function v(b){l.value=b,r.value=!1,Me(()=>{var z;(z=t.value)===null||z===void 0||z.offsetWidth,r.value=!0})}return()=>{const{clsPrefix:b}=e;return a("span",{ref:t,class:`${b}-base-slot-machine-number`},o.value!==null?a("span",{class:[`${b}-base-slot-machine-old-number ${b}-base-slot-machine-old-number--top`,u.value]},o.value):null,a("span",{class:[`${b}-base-slot-machine-current-number`,s.value]},a("span",{ref:"numberWrapper",class:[`${b}-base-slot-machine-current-number__inner`,typeof e.value!="number"&&`${b}-base-slot-machine-current-number__inner--not-number`]},n.value)),o.value!==null?a("span",{class:[`${b}-base-slot-machine-old-number ${b}-base-slot-machine-old-number--bottom`,u.value]},o.value):null)}}}),{cubicBezierEaseOut:ne}=Ro;function mt({duration:e=".2s"}={}){return[g("&.fade-up-width-expand-transition-leave-active",{transition:`
 opacity ${e} ${ne},
 max-width ${e} ${ne},
 transform ${e} ${ne}
 `}),g("&.fade-up-width-expand-transition-enter-active",{transition:`
 opacity ${e} ${ne},
 max-width ${e} ${ne},
 transform ${e} ${ne}
 `}),g("&.fade-up-width-expand-transition-enter-to",{opacity:1,transform:"translateX(0) translateY(0)"}),g("&.fade-up-width-expand-transition-enter-from",{maxWidth:"0 !important",opacity:0,transform:"translateY(60%)"}),g("&.fade-up-width-expand-transition-leave-from",{opacity:1,transform:"translateY(0)"}),g("&.fade-up-width-expand-transition-leave-to",{maxWidth:"0 !important",opacity:0,transform:"translateY(60%)"})]}const ht=g([g("@keyframes n-base-slot-machine-fade-up-in",`
 from {
 transform: translateY(60%);
 opacity: 0;
 }
 to {
 transform: translateY(0);
 opacity: 1;
 }
 `),g("@keyframes n-base-slot-machine-fade-down-in",`
 from {
 transform: translateY(-60%);
 opacity: 0;
 }
 to {
 transform: translateY(0);
 opacity: 1;
 }
 `),g("@keyframes n-base-slot-machine-fade-up-out",`
 from {
 transform: translateY(0%);
 opacity: 1;
 }
 to {
 transform: translateY(-60%);
 opacity: 0;
 }
 `),g("@keyframes n-base-slot-machine-fade-down-out",`
 from {
 transform: translateY(0%);
 opacity: 1;
 }
 to {
 transform: translateY(60%);
 opacity: 0;
 }
 `),m("base-slot-machine",`
 overflow: hidden;
 white-space: nowrap;
 display: inline-block;
 height: 18px;
 line-height: 18px;
 `,[m("base-slot-machine-number",`
 display: inline-block;
 position: relative;
 height: 18px;
 width: .6em;
 max-width: .6em;
 `,[mt({duration:".2s"}),Ho({duration:".2s",delay:"0s"}),m("base-slot-machine-old-number",`
 display: inline-block;
 opacity: 0;
 position: absolute;
 left: 0;
 right: 0;
 `,[A("top",{transform:"translateY(-100%)"}),A("bottom",{transform:"translateY(100%)"}),A("down-scroll",{animation:"n-base-slot-machine-fade-down-out .2s cubic-bezier(0, 0, .2, 1)",animationIterationCount:1}),A("up-scroll",{animation:"n-base-slot-machine-fade-up-out .2s cubic-bezier(0, 0, .2, 1)",animationIterationCount:1})]),m("base-slot-machine-current-number",`
 display: inline-block;
 position: absolute;
 left: 0;
 top: 0;
 bottom: 0;
 right: 0;
 opacity: 1;
 transform: translateY(0);
 width: .6em;
 `,[A("down-scroll",{animation:"n-base-slot-machine-fade-down-in .2s cubic-bezier(0, 0, .2, 1)",animationIterationCount:1}),A("up-scroll",{animation:"n-base-slot-machine-fade-up-in .2s cubic-bezier(0, 0, .2, 1)",animationIterationCount:1}),p("inner",`
 display: inline-block;
 position: absolute;
 right: 0;
 top: 0;
 width: .6em;
 `,[A("not-number",`
 right: unset;
 left: 0;
 `)])])])])]),ft=N({name:"BaseSlotMachine",props:{clsPrefix:{type:String,required:!0},value:{type:[Number,String],default:0},max:{type:Number,default:void 0},appeared:{type:Boolean,required:!0}},setup(e){ko("-base-slot-machine",ht,J(e,"clsPrefix"));const t=M(),o=M(),n=C(()=>{if(typeof e.value=="string")return[];if(e.value<1)return[0];const l=[];let r=e.value;for(e.max!==void 0&&(r=Math.min(e.max,r));r>=1;)l.push(r%10),r/=10,r=Math.floor(r);return l.reverse(),l});return pe(J(e,"value"),(l,r)=>{typeof l=="string"?(o.value=void 0,t.value=void 0):typeof r=="string"?(o.value=l,t.value=void 0):(o.value=l,t.value=r)}),()=>{const{value:l,clsPrefix:r}=e;return typeof l=="number"?a("span",{class:`${r}-base-slot-machine`},a(Ao,{name:"fade-up-width-expand-transition",tag:"span"},{default:()=>n.value.map((s,u)=>a(Ue,{clsPrefix:r,key:n.value.length-u-1,oldOriginalNumber:t.value,newOriginalNumber:o.value,value:s}))}),a(Ze,{key:"+",width:!0},{default:()=>e.max!==void 0&&e.max<l?a(Ue,{clsPrefix:r,value:"+"}):null})):a("span",{class:`${r}-base-slot-machine`},l)}}});function pt(e){const{borderRadius:t,avatarColor:o,cardColor:n,fontSize:l,heightTiny:r,heightSmall:s,heightMedium:u,heightLarge:d,heightHuge:v,modalColor:b,popoverColor:z}=e;return{borderRadius:t,fontSize:l,border:`2px solid ${n}`,heightTiny:r,heightSmall:s,heightMedium:u,heightLarge:d,heightHuge:v,color:ce(n,o),colorModal:ce(b,o),colorPopover:ce(z,o)}}const gt={common:de,self:pt},bt=oe("n-avatar-group"),xt=m("avatar",`
 width: var(--n-merged-size);
 height: var(--n-merged-size);
 color: #FFF;
 font-size: var(--n-font-size);
 display: inline-flex;
 position: relative;
 overflow: hidden;
 text-align: center;
 border: var(--n-border);
 border-radius: var(--n-border-radius);
 --n-merged-color: var(--n-color);
 background-color: var(--n-merged-color);
 transition:
 border-color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
`,[Po(g("&","--n-merged-color: var(--n-color-modal);")),Oo(g("&","--n-merged-color: var(--n-color-popover);")),g("img",`
 width: 100%;
 height: 100%;
 `),p("text",`
 white-space: nowrap;
 display: inline-block;
 position: absolute;
 left: 50%;
 top: 50%;
 `),m("icon",`
 vertical-align: bottom;
 font-size: calc(var(--n-merged-size) - 6px);
 `),p("text","line-height: 1.25")]),Ct=Object.assign(Object.assign({},W.props),{size:[String,Number],src:String,circle:{type:Boolean,default:void 0},objectFit:String,round:{type:Boolean,default:void 0},bordered:{type:Boolean,default:void 0},onError:Function,fallbackSrc:String,intersectionObserverOptions:Object,lazy:Boolean,onLoad:Function,renderPlaceholder:Function,renderFallback:Function,imgProps:Object,color:String}),yt=N({name:"Avatar",props:Ct,slots:Object,setup(e){const{mergedClsPrefixRef:t,inlineThemeDisabled:o}=te(e),n=M(!1);let l=null;const r=M(null),s=M(null),u=()=>{const{value:x}=r;if(x&&(l===null||l!==x.innerHTML)){l=x.innerHTML;const{value:P}=s;if(P){const{offsetWidth:B,offsetHeight:y}=P,{offsetWidth:f,offsetHeight:S}=x,E=.9,D=Math.min(B/f*E,y/S*E,1);x.style.transform=`translateX(-50%) translateY(-50%) scale(${D})`}}},d=q(bt,null),v=C(()=>{const{size:x}=e;if(x)return x;const{size:P}=d||{};return P||"medium"}),b=W("Avatar","-avatar",xt,gt,e,t),z=q(lt,null),h=C(()=>{if(d)return!0;const{round:x,circle:P}=e;return x!==void 0||P!==void 0?x||P:z?z.roundRef.value:!1}),L=C(()=>d?!0:e.bordered||!1),k=C(()=>{const x=v.value,P=h.value,B=L.value,{color:y}=e,{self:{borderRadius:f,fontSize:S,color:E,border:D,colorModal:X,colorPopover:U},common:{cubicBezierEaseInOut:ve}}=b.value;let ie;return typeof x=="number"?ie=`${x}px`:ie=b.value.self[Qe("height",x)],{"--n-font-size":S,"--n-border":B?D:"none","--n-border-radius":P?"50%":f,"--n-color":y||E,"--n-color-modal":y||X,"--n-color-popover":y||U,"--n-bezier":ve,"--n-merged-size":`var(--n-avatar-size-override, ${ie})`}}),w=o?re("avatar",C(()=>{const x=v.value,P=h.value,B=L.value,{color:y}=e;let f="";return x&&(typeof x=="number"?f+=`a${x}`:f+=x[0]),P&&(f+="b"),B&&(f+="c"),y&&(f+=eo(y)),f}),k,e):void 0,R=M(!e.lazy);Pe(()=>{if(e.lazy&&e.intersectionObserverOptions){let x;const P=Ie(()=>{x==null||x(),x=void 0,e.lazy&&(x=ct(s.value,e.intersectionObserverOptions,R))});_o(()=>{P(),x==null||x()})}}),pe(()=>{var x;return e.src||((x=e.imgProps)===null||x===void 0?void 0:x.src)},()=>{n.value=!1});const _=M(!e.lazy);return{textRef:r,selfRef:s,mergedRoundRef:h,mergedClsPrefix:t,fitTextTransform:u,cssVars:o?void 0:k,themeClass:w==null?void 0:w.themeClass,onRender:w==null?void 0:w.onRender,hasLoadError:n,shouldStartLoading:R,loaded:_,mergedOnError:x=>{if(!R.value)return;n.value=!0;const{onError:P,imgProps:{onError:B}={}}=e;P==null||P(x),B==null||B(x)},mergedOnLoad:x=>{const{onLoad:P,imgProps:{onLoad:B}={}}=e;P==null||P(x),B==null||B(x),_.value=!0}}},render(){var e,t;const{$slots:o,src:n,mergedClsPrefix:l,lazy:r,onRender:s,loaded:u,hasLoadError:d,imgProps:v={}}=this;s==null||s();let b;const z=!u&&!d&&(this.renderPlaceholder?this.renderPlaceholder():(t=(e=this.$slots).placeholder)===null||t===void 0?void 0:t.call(e));return this.hasLoadError?b=this.renderFallback?this.renderFallback():Ae(o.fallback,()=>[a("img",{src:this.fallbackSrc,style:{objectFit:this.objectFit}})]):b=Lo(o.default,h=>{if(h)return a(Je,{onResize:this.fitTextTransform},{default:()=>a("span",{ref:"textRef",class:`${l}-avatar__text`},h)});if(n||v.src){const L=this.src||v.src;return a("img",Object.assign(Object.assign({},v),{loading:st&&!this.intersectionObserverOptions&&r?"lazy":"eager",src:r&&this.intersectionObserverOptions?this.shouldStartLoading?L:void 0:L,"data-image-src":L,onLoad:this.mergedOnLoad,onError:this.mergedOnError,style:[v.style||"",{objectFit:this.objectFit},z?{height:"0",width:"0",visibility:"hidden",position:"absolute"}:""]}))}}),a("span",{ref:"selfRef",class:[`${l}-avatar`,this.themeClass],style:this.cssVars},b,r&&z)}});function wt(e){const{errorColor:t,infoColor:o,successColor:n,warningColor:l,fontFamily:r}=e;return{color:t,colorInfo:o,colorSuccess:n,colorError:t,colorWarning:l,fontSize:"12px",fontFamily:r}}const zt={common:de,self:wt},It=g([g("@keyframes badge-wave-spread",{from:{boxShadow:"0 0 0.5px 0px var(--n-ripple-color)",opacity:.6},to:{boxShadow:"0 0 0.5px 4.5px var(--n-ripple-color)",opacity:0}}),m("badge",`
 display: inline-flex;
 position: relative;
 vertical-align: middle;
 font-family: var(--n-font-family);
 `,[A("as-is",[m("badge-sup",{position:"static",transform:"translateX(0)"},[Ee({transformOrigin:"left bottom",originalTransform:"translateX(0)"})])]),A("dot",[m("badge-sup",`
 height: 8px;
 width: 8px;
 padding: 0;
 min-width: 8px;
 left: 100%;
 bottom: calc(100% - 4px);
 `,[g("::before","border-radius: 4px;")])]),m("badge-sup",`
 background: var(--n-color);
 transition:
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
 color: #FFF;
 position: absolute;
 height: 18px;
 line-height: 18px;
 border-radius: 9px;
 padding: 0 6px;
 text-align: center;
 font-size: var(--n-font-size);
 transform: translateX(-50%);
 left: 100%;
 bottom: calc(100% - 9px);
 font-variant-numeric: tabular-nums;
 z-index: 2;
 display: flex;
 align-items: center;
 `,[Ee({transformOrigin:"left bottom",originalTransform:"translateX(-50%)"}),m("base-wave",{zIndex:1,animationDuration:"2s",animationIterationCount:"infinite",animationDelay:"1s",animationTimingFunction:"var(--n-ripple-bezier)",animationName:"badge-wave-spread"}),g("&::before",`
 opacity: 0;
 transform: scale(1);
 border-radius: 9px;
 content: "";
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 `)])])]),St=Object.assign(Object.assign({},W.props),{value:[String,Number],max:Number,dot:Boolean,type:{type:String,default:"default"},show:{type:Boolean,default:!0},showZero:Boolean,processing:Boolean,color:String,offset:Array}),Rt=N({name:"Badge",props:St,setup(e,{slots:t}){const{mergedClsPrefixRef:o,inlineThemeDisabled:n,mergedRtlRef:l}=te(e),r=W("Badge","-badge",It,zt,e,o),s=M(!1),u=()=>{s.value=!0},d=()=>{s.value=!1},v=C(()=>e.show&&(e.dot||e.value!==void 0&&!(!e.showZero&&Number(e.value)<=0)||!Bo(t.value)));Pe(()=>{v.value&&(s.value=!0)});const b=No("Badge",l,o),z=C(()=>{const{type:k,color:w}=e,{common:{cubicBezierEaseInOut:R,cubicBezierEaseOut:_},self:{[Qe("color",k)]:x,fontFamily:P,fontSize:B}}=r.value;return{"--n-font-size":B,"--n-font-family":P,"--n-color":w||x,"--n-ripple-color":w||x,"--n-bezier":R,"--n-ripple-bezier":_}}),h=n?re("badge",C(()=>{let k="";const{type:w,color:R}=e;return w&&(k+=w[0]),R&&(k+=eo(R)),k}),z,e):void 0,L=C(()=>{const{offset:k}=e;if(!k)return;const[w,R]=k,_=typeof w=="number"?`${w}px`:w,x=typeof R=="number"?`${R}px`:R;return{transform:`translate(calc(${b!=null&&b.value?"50%":"-50%"} + ${_}), ${x})`}});return{rtlEnabled:b,mergedClsPrefix:o,appeared:s,showBadge:v,handleAfterEnter:u,handleAfterLeave:d,cssVars:n?void 0:z,themeClass:h==null?void 0:h.themeClass,onRender:h==null?void 0:h.onRender,offsetStyle:L}},render(){var e;const{mergedClsPrefix:t,onRender:o,themeClass:n,$slots:l}=this;o==null||o();const r=(e=l.default)===null||e===void 0?void 0:e.call(l);return a("div",{class:[`${t}-badge`,this.rtlEnabled&&`${t}-badge--rtl`,n,{[`${t}-badge--dot`]:this.dot,[`${t}-badge--as-is`]:!r}],style:this.cssVars},r,a(To,{name:"fade-in-scale-up-transition",onAfterEnter:this.handleAfterEnter,onAfterLeave:this.handleAfterLeave},{default:()=>this.showBadge?a("sup",{class:`${t}-badge-sup`,title:rt(this.value),style:this.offsetStyle},Ae(l.value,()=>[this.dot?null:a(ft,{clsPrefix:t,appeared:this.appeared,max:this.max,value:this.value})]),this.processing?a($o,{clsPrefix:t}):null):null}))}}),Ht={fontWeightActive:"400"};function kt(e){const{fontSize:t,textColor3:o,textColor2:n,borderRadius:l,buttonColor2Hover:r,buttonColor2Pressed:s}=e;return Object.assign(Object.assign({},Ht),{fontSize:t,itemLineHeight:"1.25",itemTextColor:o,itemTextColorHover:n,itemTextColorPressed:n,itemTextColorActive:n,itemBorderRadius:l,itemColorHover:r,itemColorPressed:s,separatorColor:o})}const At={common:de,self:kt},Pt=m("breadcrumb",`
 white-space: nowrap;
 cursor: default;
 line-height: var(--n-item-line-height);
`,[g("ul",`
 list-style: none;
 padding: 0;
 margin: 0;
 `),g("a",`
 color: inherit;
 text-decoration: inherit;
 `),m("breadcrumb-item",`
 font-size: var(--n-font-size);
 transition: color .3s var(--n-bezier);
 display: inline-flex;
 align-items: center;
 `,[m("icon",`
 font-size: 18px;
 vertical-align: -.2em;
 transition: color .3s var(--n-bezier);
 color: var(--n-item-text-color);
 `),g("&:not(:last-child)",[A("clickable",[p("link",`
 cursor: pointer;
 `,[g("&:hover",`
 background-color: var(--n-item-color-hover);
 `),g("&:active",`
 background-color: var(--n-item-color-pressed); 
 `)])])]),p("link",`
 padding: 4px;
 border-radius: var(--n-item-border-radius);
 transition:
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
 color: var(--n-item-text-color);
 position: relative;
 `,[g("&:hover",`
 color: var(--n-item-text-color-hover);
 `,[m("icon",`
 color: var(--n-item-text-color-hover);
 `)]),g("&:active",`
 color: var(--n-item-text-color-pressed);
 `,[m("icon",`
 color: var(--n-item-text-color-pressed);
 `)])]),p("separator",`
 margin: 0 8px;
 color: var(--n-separator-color);
 transition: color .3s var(--n-bezier);
 user-select: none;
 -webkit-user-select: none;
 `),g("&:last-child",[p("link",`
 font-weight: var(--n-font-weight-active);
 cursor: unset;
 color: var(--n-item-text-color-active);
 `,[m("icon",`
 color: var(--n-item-text-color-active);
 `)]),p("separator",`
 display: none;
 `)])])]),ao=oe("n-breadcrumb"),Ot=Object.assign(Object.assign({},W.props),{separator:{type:String,default:"/"}}),Lt=N({name:"Breadcrumb",props:Ot,setup(e){const{mergedClsPrefixRef:t,inlineThemeDisabled:o}=te(e),n=W("Breadcrumb","-breadcrumb",Pt,At,e,t);ee(ao,{separatorRef:J(e,"separator"),mergedClsPrefixRef:t});const l=C(()=>{const{common:{cubicBezierEaseInOut:s},self:{separatorColor:u,itemTextColor:d,itemTextColorHover:v,itemTextColorPressed:b,itemTextColorActive:z,fontSize:h,fontWeightActive:L,itemBorderRadius:k,itemColorHover:w,itemColorPressed:R,itemLineHeight:_}}=n.value;return{"--n-font-size":h,"--n-bezier":s,"--n-item-text-color":d,"--n-item-text-color-hover":v,"--n-item-text-color-pressed":b,"--n-item-text-color-active":z,"--n-separator-color":u,"--n-item-color-hover":w,"--n-item-color-pressed":R,"--n-item-border-radius":k,"--n-font-weight-active":L,"--n-item-line-height":_}}),r=o?re("breadcrumb",void 0,l,e):void 0;return{mergedClsPrefix:t,cssVars:o?void 0:l,themeClass:r==null?void 0:r.themeClass,onRender:r==null?void 0:r.onRender}},render(){var e;return(e=this.onRender)===null||e===void 0||e.call(this),a("nav",{class:[`${this.mergedClsPrefix}-breadcrumb`,this.themeClass],style:this.cssVars,"aria-label":"Breadcrumb"},a("ul",null,this.$slots))}});function _t(e=Eo?window:null){const t=()=>{const{hash:l,host:r,hostname:s,href:u,origin:d,pathname:v,port:b,protocol:z,search:h}=(e==null?void 0:e.location)||{};return{hash:l,host:r,hostname:s,href:u,origin:d,pathname:v,port:b,protocol:z,search:h}},o=M(t()),n=()=>{o.value=t()};return Pe(()=>{e&&(e.addEventListener("popstate",n),e.addEventListener("hashchange",n))}),Mo(()=>{e&&(e.removeEventListener("popstate",n),e.removeEventListener("hashchange",n))}),o}const Tt={separator:String,href:String,clickable:{type:Boolean,default:!0},showSeparator:{type:Boolean,default:!0},onClick:Function},$t=N({name:"BreadcrumbItem",props:Tt,slots:Object,setup(e,{slots:t}){const o=q(ao,null);if(!o)return()=>null;const{separatorRef:n,mergedClsPrefixRef:l}=o,r=_t(),s=C(()=>e.href?"a":"span"),u=C(()=>r.value.href===e.href?"location":null);return()=>{const{value:d}=l;return a("li",{class:[`${d}-breadcrumb-item`,e.clickable&&`${d}-breadcrumb-item--clickable`]},a(s.value,{class:`${d}-breadcrumb-item__link`,"aria-current":u.value,href:e.href,onClick:e.onClick},t),e.showSeparator&&a("span",{class:`${d}-breadcrumb-item__separator`,"aria-hidden":"true"},Ae(t.separator,()=>{var v;return[(v=e.separator)!==null&&v!==void 0?v:n.value]})))}}});function Nt(e){const{baseColor:t,textColor2:o,bodyColor:n,cardColor:l,dividerColor:r,actionColor:s,scrollbarColor:u,scrollbarColorHover:d,invertedColor:v}=e;return{textColor:o,textColorInverted:"#FFF",color:n,colorEmbedded:s,headerColor:l,headerColorInverted:v,footerColor:s,footerColorInverted:v,headerBorderColor:r,headerBorderColorInverted:v,footerBorderColor:r,footerBorderColorInverted:v,siderBorderColor:r,siderBorderColorInverted:v,siderColor:l,siderColorInverted:v,siderToggleButtonBorder:`1px solid ${r}`,siderToggleButtonColor:t,siderToggleButtonIconColor:o,siderToggleButtonIconColorInverted:o,siderToggleBarColor:ce(n,u),siderToggleBarColorHover:ce(n,d),__invertScrollbar:"true"}}const Le=oo({name:"Layout",common:de,peers:{Scrollbar:Fo},self:Nt});function Bt(e,t,o,n){return{itemColorHoverInverted:"#0000",itemColorActiveInverted:t,itemColorActiveHoverInverted:t,itemColorActiveCollapsedInverted:t,itemTextColorInverted:e,itemTextColorHoverInverted:o,itemTextColorChildActiveInverted:o,itemTextColorChildActiveHoverInverted:o,itemTextColorActiveInverted:o,itemTextColorActiveHoverInverted:o,itemTextColorHorizontalInverted:e,itemTextColorHoverHorizontalInverted:o,itemTextColorChildActiveHorizontalInverted:o,itemTextColorChildActiveHoverHorizontalInverted:o,itemTextColorActiveHorizontalInverted:o,itemTextColorActiveHoverHorizontalInverted:o,itemIconColorInverted:e,itemIconColorHoverInverted:o,itemIconColorActiveInverted:o,itemIconColorActiveHoverInverted:o,itemIconColorChildActiveInverted:o,itemIconColorChildActiveHoverInverted:o,itemIconColorCollapsedInverted:e,itemIconColorHorizontalInverted:e,itemIconColorHoverHorizontalInverted:o,itemIconColorActiveHorizontalInverted:o,itemIconColorActiveHoverHorizontalInverted:o,itemIconColorChildActiveHorizontalInverted:o,itemIconColorChildActiveHoverHorizontalInverted:o,arrowColorInverted:e,arrowColorHoverInverted:o,arrowColorActiveInverted:o,arrowColorActiveHoverInverted:o,arrowColorChildActiveInverted:o,arrowColorChildActiveHoverInverted:o,groupTextColorInverted:n}}function Mt(e){const{borderRadius:t,textColor3:o,primaryColor:n,textColor2:l,textColor1:r,fontSize:s,dividerColor:u,hoverColor:d,primaryColorHover:v}=e;return Object.assign({borderRadius:t,color:"#0000",groupTextColor:o,itemColorHover:d,itemColorActive:ge(n,{alpha:.1}),itemColorActiveHover:ge(n,{alpha:.1}),itemColorActiveCollapsed:ge(n,{alpha:.1}),itemTextColor:l,itemTextColorHover:l,itemTextColorActive:n,itemTextColorActiveHover:n,itemTextColorChildActive:n,itemTextColorChildActiveHover:n,itemTextColorHorizontal:l,itemTextColorHoverHorizontal:v,itemTextColorActiveHorizontal:n,itemTextColorActiveHoverHorizontal:n,itemTextColorChildActiveHorizontal:n,itemTextColorChildActiveHoverHorizontal:n,itemIconColor:r,itemIconColorHover:r,itemIconColorActive:n,itemIconColorActiveHover:n,itemIconColorChildActive:n,itemIconColorChildActiveHover:n,itemIconColorCollapsed:r,itemIconColorHorizontal:r,itemIconColorHoverHorizontal:v,itemIconColorActiveHorizontal:n,itemIconColorActiveHoverHorizontal:n,itemIconColorChildActiveHorizontal:n,itemIconColorChildActiveHoverHorizontal:n,itemHeight:"42px",arrowColor:l,arrowColorHover:l,arrowColorActive:n,arrowColorActiveHover:n,arrowColorChildActive:n,arrowColorChildActiveHover:n,colorInverted:"#0000",borderColorHorizontal:"#0000",fontSize:s,dividerColor:u},Bt("#BBB",n,"#FFF","#AAA"))}const Et=oo({name:"Menu",common:de,peers:{Tooltip:ot,Dropdown:Jo},self:Mt}),so=oe("n-layout-sider"),_e={type:String,default:"static"},Ft=m("layout",`
 color: var(--n-text-color);
 background-color: var(--n-color);
 box-sizing: border-box;
 position: relative;
 z-index: auto;
 flex: auto;
 overflow: hidden;
 transition:
 box-shadow .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
`,[m("layout-scroll-container",`
 overflow-x: hidden;
 box-sizing: border-box;
 height: 100%;
 `),A("absolute-positioned",`
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 `)]),jt={embedded:Boolean,position:_e,nativeScrollbar:{type:Boolean,default:!0},scrollbarProps:Object,onScroll:Function,contentClass:String,contentStyle:{type:[String,Object],default:""},hasSider:Boolean,siderPlacement:{type:String,default:"left"}},co=oe("n-layout");function uo(e){return N({name:e?"LayoutContent":"Layout",props:Object.assign(Object.assign({},W.props),jt),setup(t){const o=M(null),n=M(null),{mergedClsPrefixRef:l,inlineThemeDisabled:r}=te(t),s=W("Layout","-layout",Ft,Le,t,l);function u(w,R){if(t.nativeScrollbar){const{value:_}=o;_&&(R===void 0?_.scrollTo(w):_.scrollTo(w,R))}else{const{value:_}=n;_&&_.scrollTo(w,R)}}ee(co,t);let d=0,v=0;const b=w=>{var R;const _=w.target;d=_.scrollLeft,v=_.scrollTop,(R=t.onScroll)===null||R===void 0||R.call(t,w)};ro(()=>{if(t.nativeScrollbar){const w=o.value;w&&(w.scrollTop=v,w.scrollLeft=d)}});const z={display:"flex",flexWrap:"nowrap",width:"100%",flexDirection:"row"},h={scrollTo:u},L=C(()=>{const{common:{cubicBezierEaseInOut:w},self:R}=s.value;return{"--n-bezier":w,"--n-color":t.embedded?R.colorEmbedded:R.color,"--n-text-color":R.textColor}}),k=r?re("layout",C(()=>t.embedded?"e":""),L,t):void 0;return Object.assign({mergedClsPrefix:l,scrollableElRef:o,scrollbarInstRef:n,hasSiderStyle:z,mergedTheme:s,handleNativeElScroll:b,cssVars:r?void 0:L,themeClass:k==null?void 0:k.themeClass,onRender:k==null?void 0:k.onRender},h)},render(){var t;const{mergedClsPrefix:o,hasSider:n}=this;(t=this.onRender)===null||t===void 0||t.call(this);const l=n?this.hasSiderStyle:void 0,r=[this.themeClass,e&&`${o}-layout-content`,`${o}-layout`,`${o}-layout--${this.position}-positioned`];return a("div",{class:r,style:this.cssVars},this.nativeScrollbar?a("div",{ref:"scrollableElRef",class:[`${o}-layout-scroll-container`,this.contentClass],style:[this.contentStyle,l],onScroll:this.handleNativeElScroll},this.$slots):a(to,Object.assign({},this.scrollbarProps,{onScroll:this.onScroll,ref:"scrollbarInstRef",theme:this.mergedTheme.peers.Scrollbar,themeOverrides:this.mergedTheme.peerOverrides.Scrollbar,contentClass:this.contentClass,contentStyle:[this.contentStyle,l]}),this.$slots))}})}const Ye=uo(!1),Vt=uo(!0),Kt=m("layout-header",`
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 box-sizing: border-box;
 width: 100%;
 background-color: var(--n-color);
 color: var(--n-text-color);
`,[A("absolute-positioned",`
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 `),A("bordered",`
 border-bottom: solid 1px var(--n-border-color);
 `)]),Dt={position:_e,inverted:Boolean,bordered:{type:Boolean,default:!1}},Ut=N({name:"LayoutHeader",props:Object.assign(Object.assign({},W.props),Dt),setup(e){const{mergedClsPrefixRef:t,inlineThemeDisabled:o}=te(e),n=W("Layout","-layout-header",Kt,Le,e,t),l=C(()=>{const{common:{cubicBezierEaseInOut:s},self:u}=n.value,d={"--n-bezier":s};return e.inverted?(d["--n-color"]=u.headerColorInverted,d["--n-text-color"]=u.textColorInverted,d["--n-border-color"]=u.headerBorderColorInverted):(d["--n-color"]=u.headerColor,d["--n-text-color"]=u.textColor,d["--n-border-color"]=u.headerBorderColor),d}),r=o?re("layout-header",C(()=>e.inverted?"a":"b"),l,e):void 0;return{mergedClsPrefix:t,cssVars:o?void 0:l,themeClass:r==null?void 0:r.themeClass,onRender:r==null?void 0:r.onRender}},render(){var e;const{mergedClsPrefix:t}=this;return(e=this.onRender)===null||e===void 0||e.call(this),a("div",{class:[`${t}-layout-header`,this.themeClass,this.position&&`${t}-layout-header--${this.position}-positioned`,this.bordered&&`${t}-layout-header--bordered`],style:this.cssVars},this.$slots)}}),Yt=m("layout-sider",`
 flex-shrink: 0;
 box-sizing: border-box;
 position: relative;
 z-index: 1;
 color: var(--n-text-color);
 transition:
 color .3s var(--n-bezier),
 border-color .3s var(--n-bezier),
 min-width .3s var(--n-bezier),
 max-width .3s var(--n-bezier),
 transform .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 background-color: var(--n-color);
 display: flex;
 justify-content: flex-end;
`,[A("bordered",[p("border",`
 content: "";
 position: absolute;
 top: 0;
 bottom: 0;
 width: 1px;
 background-color: var(--n-border-color);
 transition: background-color .3s var(--n-bezier);
 `)]),p("left-placement",[A("bordered",[p("border",`
 right: 0;
 `)])]),A("right-placement",`
 justify-content: flex-start;
 `,[A("bordered",[p("border",`
 left: 0;
 `)]),A("collapsed",[m("layout-toggle-button",[m("base-icon",`
 transform: rotate(180deg);
 `)]),m("layout-toggle-bar",[g("&:hover",[p("top",{transform:"rotate(-12deg) scale(1.15) translateY(-2px)"}),p("bottom",{transform:"rotate(12deg) scale(1.15) translateY(2px)"})])])]),m("layout-toggle-button",`
 left: 0;
 transform: translateX(-50%) translateY(-50%);
 `,[m("base-icon",`
 transform: rotate(0);
 `)]),m("layout-toggle-bar",`
 left: -28px;
 transform: rotate(180deg);
 `,[g("&:hover",[p("top",{transform:"rotate(12deg) scale(1.15) translateY(-2px)"}),p("bottom",{transform:"rotate(-12deg) scale(1.15) translateY(2px)"})])])]),A("collapsed",[m("layout-toggle-bar",[g("&:hover",[p("top",{transform:"rotate(-12deg) scale(1.15) translateY(-2px)"}),p("bottom",{transform:"rotate(12deg) scale(1.15) translateY(2px)"})])]),m("layout-toggle-button",[m("base-icon",`
 transform: rotate(0);
 `)])]),m("layout-toggle-button",`
 transition:
 color .3s var(--n-bezier),
 right .3s var(--n-bezier),
 left .3s var(--n-bezier),
 border-color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 cursor: pointer;
 width: 24px;
 height: 24px;
 position: absolute;
 top: 50%;
 right: 0;
 border-radius: 50%;
 display: flex;
 align-items: center;
 justify-content: center;
 font-size: 18px;
 color: var(--n-toggle-button-icon-color);
 border: var(--n-toggle-button-border);
 background-color: var(--n-toggle-button-color);
 box-shadow: 0 2px 4px 0px rgba(0, 0, 0, .06);
 transform: translateX(50%) translateY(-50%);
 z-index: 1;
 `,[m("base-icon",`
 transition: transform .3s var(--n-bezier);
 transform: rotate(180deg);
 `)]),m("layout-toggle-bar",`
 cursor: pointer;
 height: 72px;
 width: 32px;
 position: absolute;
 top: calc(50% - 36px);
 right: -28px;
 `,[p("top, bottom",`
 position: absolute;
 width: 4px;
 border-radius: 2px;
 height: 38px;
 left: 14px;
 transition: 
 background-color .3s var(--n-bezier),
 transform .3s var(--n-bezier);
 `),p("bottom",`
 position: absolute;
 top: 34px;
 `),g("&:hover",[p("top",{transform:"rotate(12deg) scale(1.15) translateY(-2px)"}),p("bottom",{transform:"rotate(-12deg) scale(1.15) translateY(2px)"})]),p("top, bottom",{backgroundColor:"var(--n-toggle-bar-color)"}),g("&:hover",[p("top, bottom",{backgroundColor:"var(--n-toggle-bar-color-hover)"})])]),p("border",`
 position: absolute;
 top: 0;
 right: 0;
 bottom: 0;
 width: 1px;
 transition: background-color .3s var(--n-bezier);
 `),m("layout-sider-scroll-container",`
 flex-grow: 1;
 flex-shrink: 0;
 box-sizing: border-box;
 height: 100%;
 opacity: 0;
 transition: opacity .3s var(--n-bezier);
 max-width: 100%;
 `),A("show-content",[m("layout-sider-scroll-container",{opacity:1})]),A("absolute-positioned",`
 position: absolute;
 left: 0;
 top: 0;
 bottom: 0;
 `)]),Wt=N({props:{clsPrefix:{type:String,required:!0},onClick:Function},render(){const{clsPrefix:e}=this;return a("div",{onClick:this.onClick,class:`${e}-layout-toggle-bar`},a("div",{class:`${e}-layout-toggle-bar__top`}),a("div",{class:`${e}-layout-toggle-bar__bottom`}))}}),Gt=N({name:"LayoutToggleButton",props:{clsPrefix:{type:String,required:!0},onClick:Function},render(){const{clsPrefix:e}=this;return a("div",{class:`${e}-layout-toggle-button`,onClick:this.onClick},a(no,{clsPrefix:e},{default:()=>a(Qo,null)}))}}),qt={position:_e,bordered:Boolean,collapsedWidth:{type:Number,default:48},width:{type:[Number,String],default:272},contentClass:String,contentStyle:{type:[String,Object],default:""},collapseMode:{type:String,default:"transform"},collapsed:{type:Boolean,default:void 0},defaultCollapsed:Boolean,showCollapsedContent:{type:Boolean,default:!0},showTrigger:{type:[Boolean,String],default:!1},nativeScrollbar:{type:Boolean,default:!0},inverted:Boolean,scrollbarProps:Object,triggerClass:String,triggerStyle:[String,Object],collapsedTriggerClass:String,collapsedTriggerStyle:[String,Object],"onUpdate:collapsed":[Function,Array],onUpdateCollapsed:[Function,Array],onAfterEnter:Function,onAfterLeave:Function,onExpand:[Function,Array],onCollapse:[Function,Array],onScroll:Function},Xt=N({name:"LayoutSider",props:Object.assign(Object.assign({},W.props),qt),setup(e){const t=q(co),o=M(null),n=M(null),l=M(e.defaultCollapsed),r=Re(J(e,"collapsed"),l),s=C(()=>we(r.value?e.collapsedWidth:e.width)),u=C(()=>e.collapseMode!=="transform"?{}:{minWidth:we(e.width)}),d=C(()=>t?t.siderPlacement:"left");function v(y,f){if(e.nativeScrollbar){const{value:S}=o;S&&(f===void 0?S.scrollTo(y):S.scrollTo(y,f))}else{const{value:S}=n;S&&S.scrollTo(y,f)}}function b(){const{"onUpdate:collapsed":y,onUpdateCollapsed:f,onExpand:S,onCollapse:E}=e,{value:D}=r;f&&G(f,!D),y&&G(y,!D),l.value=!D,D?S&&G(S):E&&G(E)}let z=0,h=0;const L=y=>{var f;const S=y.target;z=S.scrollLeft,h=S.scrollTop,(f=e.onScroll)===null||f===void 0||f.call(e,y)};ro(()=>{if(e.nativeScrollbar){const y=o.value;y&&(y.scrollTop=h,y.scrollLeft=z)}}),ee(so,{collapsedRef:r,collapseModeRef:J(e,"collapseMode")});const{mergedClsPrefixRef:k,inlineThemeDisabled:w}=te(e),R=W("Layout","-layout-sider",Yt,Le,e,k);function _(y){var f,S;y.propertyName==="max-width"&&(r.value?(f=e.onAfterLeave)===null||f===void 0||f.call(e):(S=e.onAfterEnter)===null||S===void 0||S.call(e))}const x={scrollTo:v},P=C(()=>{const{common:{cubicBezierEaseInOut:y},self:f}=R.value,{siderToggleButtonColor:S,siderToggleButtonBorder:E,siderToggleBarColor:D,siderToggleBarColorHover:X}=f,U={"--n-bezier":y,"--n-toggle-button-color":S,"--n-toggle-button-border":E,"--n-toggle-bar-color":D,"--n-toggle-bar-color-hover":X};return e.inverted?(U["--n-color"]=f.siderColorInverted,U["--n-text-color"]=f.textColorInverted,U["--n-border-color"]=f.siderBorderColorInverted,U["--n-toggle-button-icon-color"]=f.siderToggleButtonIconColorInverted,U.__invertScrollbar=f.__invertScrollbar):(U["--n-color"]=f.siderColor,U["--n-text-color"]=f.textColor,U["--n-border-color"]=f.siderBorderColor,U["--n-toggle-button-icon-color"]=f.siderToggleButtonIconColor),U}),B=w?re("layout-sider",C(()=>e.inverted?"a":"b"),P,e):void 0;return Object.assign({scrollableElRef:o,scrollbarInstRef:n,mergedClsPrefix:k,mergedTheme:R,styleMaxWidth:s,mergedCollapsed:r,scrollContainerStyle:u,siderPlacement:d,handleNativeElScroll:L,handleTransitionend:_,handleTriggerClick:b,inlineThemeDisabled:w,cssVars:P,themeClass:B==null?void 0:B.themeClass,onRender:B==null?void 0:B.onRender},x)},render(){var e;const{mergedClsPrefix:t,mergedCollapsed:o,showTrigger:n}=this;return(e=this.onRender)===null||e===void 0||e.call(this),a("aside",{class:[`${t}-layout-sider`,this.themeClass,`${t}-layout-sider--${this.position}-positioned`,`${t}-layout-sider--${this.siderPlacement}-placement`,this.bordered&&`${t}-layout-sider--bordered`,o&&`${t}-layout-sider--collapsed`,(!o||this.showCollapsedContent)&&`${t}-layout-sider--show-content`],onTransitionend:this.handleTransitionend,style:[this.inlineThemeDisabled?void 0:this.cssVars,{maxWidth:this.styleMaxWidth,width:we(this.width)}]},this.nativeScrollbar?a("div",{class:[`${t}-layout-sider-scroll-container`,this.contentClass],onScroll:this.handleNativeElScroll,style:[this.scrollContainerStyle,{overflow:"auto"},this.contentStyle],ref:"scrollableElRef"},this.$slots):a(to,Object.assign({},this.scrollbarProps,{onScroll:this.onScroll,ref:"scrollbarInstRef",style:this.scrollContainerStyle,contentStyle:this.contentStyle,contentClass:this.contentClass,theme:this.mergedTheme.peers.Scrollbar,themeOverrides:this.mergedTheme.peerOverrides.Scrollbar,builtinThemeOverrides:this.inverted&&this.cssVars.__invertScrollbar==="true"?{colorHover:"rgba(255, 255, 255, .4)",color:"rgba(255, 255, 255, .3)"}:void 0}),this.$slots),n?n==="bar"?a(Wt,{clsPrefix:t,class:o?this.collapsedTriggerClass:this.triggerClass,style:o?this.collapsedTriggerStyle:this.triggerStyle,onClick:this.handleTriggerClick}):a(Gt,{clsPrefix:t,class:o?this.collapsedTriggerClass:this.triggerClass,style:o?this.collapsedTriggerStyle:this.triggerStyle,onClick:this.handleTriggerClick}):null,this.bordered?a("div",{class:`${t}-layout-sider__border`}):null)}}),ue=oe("n-menu"),vo=oe("n-submenu"),Te=oe("n-menu-item-group"),We=[g("&::before","background-color: var(--n-item-color-hover);"),p("arrow",`
 color: var(--n-arrow-color-hover);
 `),p("icon",`
 color: var(--n-item-icon-color-hover);
 `),m("menu-item-content-header",`
 color: var(--n-item-text-color-hover);
 `,[g("a",`
 color: var(--n-item-text-color-hover);
 `),p("extra",`
 color: var(--n-item-text-color-hover);
 `)])],Ge=[p("icon",`
 color: var(--n-item-icon-color-hover-horizontal);
 `),m("menu-item-content-header",`
 color: var(--n-item-text-color-hover-horizontal);
 `,[g("a",`
 color: var(--n-item-text-color-hover-horizontal);
 `),p("extra",`
 color: var(--n-item-text-color-hover-horizontal);
 `)])],Zt=g([m("menu",`
 background-color: var(--n-color);
 color: var(--n-item-text-color);
 overflow: hidden;
 transition: background-color .3s var(--n-bezier);
 box-sizing: border-box;
 font-size: var(--n-font-size);
 padding-bottom: 6px;
 `,[A("horizontal",`
 max-width: 100%;
 width: 100%;
 display: flex;
 overflow: hidden;
 padding-bottom: 0;
 `,[m("submenu","margin: 0;"),m("menu-item","margin: 0;"),m("menu-item-content",`
 padding: 0 20px;
 border-bottom: 2px solid #0000;
 `,[g("&::before","display: none;"),A("selected","border-bottom: 2px solid var(--n-border-color-horizontal)")]),m("menu-item-content",[A("selected",[p("icon","color: var(--n-item-icon-color-active-horizontal);"),m("menu-item-content-header",`
 color: var(--n-item-text-color-active-horizontal);
 `,[g("a","color: var(--n-item-text-color-active-horizontal);"),p("extra","color: var(--n-item-text-color-active-horizontal);")])]),A("child-active",`
 border-bottom: 2px solid var(--n-border-color-horizontal);
 `,[m("menu-item-content-header",`
 color: var(--n-item-text-color-child-active-horizontal);
 `,[g("a",`
 color: var(--n-item-text-color-child-active-horizontal);
 `),p("extra",`
 color: var(--n-item-text-color-child-active-horizontal);
 `)]),p("icon",`
 color: var(--n-item-icon-color-child-active-horizontal);
 `)]),ae("disabled",[ae("selected, child-active",[g("&:focus-within",Ge)]),A("selected",[Q(null,[p("icon","color: var(--n-item-icon-color-active-hover-horizontal);"),m("menu-item-content-header",`
 color: var(--n-item-text-color-active-hover-horizontal);
 `,[g("a","color: var(--n-item-text-color-active-hover-horizontal);"),p("extra","color: var(--n-item-text-color-active-hover-horizontal);")])])]),A("child-active",[Q(null,[p("icon","color: var(--n-item-icon-color-child-active-hover-horizontal);"),m("menu-item-content-header",`
 color: var(--n-item-text-color-child-active-hover-horizontal);
 `,[g("a","color: var(--n-item-text-color-child-active-hover-horizontal);"),p("extra","color: var(--n-item-text-color-child-active-hover-horizontal);")])])]),Q("border-bottom: 2px solid var(--n-border-color-horizontal);",Ge)]),m("menu-item-content-header",[g("a","color: var(--n-item-text-color-horizontal);")])])]),ae("responsive",[m("menu-item-content-header",`
 overflow: hidden;
 text-overflow: ellipsis;
 `)]),A("collapsed",[m("menu-item-content",[A("selected",[g("&::before",`
 background-color: var(--n-item-color-active-collapsed) !important;
 `)]),m("menu-item-content-header","opacity: 0;"),p("arrow","opacity: 0;"),p("icon","color: var(--n-item-icon-color-collapsed);")])]),m("menu-item",`
 height: var(--n-item-height);
 margin-top: 6px;
 position: relative;
 `),m("menu-item-content",`
 box-sizing: border-box;
 line-height: 1.75;
 height: 100%;
 display: grid;
 grid-template-areas: "icon content arrow";
 grid-template-columns: auto 1fr auto;
 align-items: center;
 cursor: pointer;
 position: relative;
 padding-right: 18px;
 transition:
 background-color .3s var(--n-bezier),
 padding-left .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `,[g("> *","z-index: 1;"),g("&::before",`
 z-index: auto;
 content: "";
 background-color: #0000;
 position: absolute;
 left: 8px;
 right: 8px;
 top: 0;
 bottom: 0;
 pointer-events: none;
 border-radius: var(--n-border-radius);
 transition: background-color .3s var(--n-bezier);
 `),A("disabled",`
 opacity: .45;
 cursor: not-allowed;
 `),A("collapsed",[p("arrow","transform: rotate(0);")]),A("selected",[g("&::before","background-color: var(--n-item-color-active);"),p("arrow","color: var(--n-arrow-color-active);"),p("icon","color: var(--n-item-icon-color-active);"),m("menu-item-content-header",`
 color: var(--n-item-text-color-active);
 `,[g("a","color: var(--n-item-text-color-active);"),p("extra","color: var(--n-item-text-color-active);")])]),A("child-active",[m("menu-item-content-header",`
 color: var(--n-item-text-color-child-active);
 `,[g("a",`
 color: var(--n-item-text-color-child-active);
 `),p("extra",`
 color: var(--n-item-text-color-child-active);
 `)]),p("arrow",`
 color: var(--n-arrow-color-child-active);
 `),p("icon",`
 color: var(--n-item-icon-color-child-active);
 `)]),ae("disabled",[ae("selected, child-active",[g("&:focus-within",We)]),A("selected",[Q(null,[p("arrow","color: var(--n-arrow-color-active-hover);"),p("icon","color: var(--n-item-icon-color-active-hover);"),m("menu-item-content-header",`
 color: var(--n-item-text-color-active-hover);
 `,[g("a","color: var(--n-item-text-color-active-hover);"),p("extra","color: var(--n-item-text-color-active-hover);")])])]),A("child-active",[Q(null,[p("arrow","color: var(--n-arrow-color-child-active-hover);"),p("icon","color: var(--n-item-icon-color-child-active-hover);"),m("menu-item-content-header",`
 color: var(--n-item-text-color-child-active-hover);
 `,[g("a","color: var(--n-item-text-color-child-active-hover);"),p("extra","color: var(--n-item-text-color-child-active-hover);")])])]),A("selected",[Q(null,[g("&::before","background-color: var(--n-item-color-active-hover);")])]),Q(null,We)]),p("icon",`
 grid-area: icon;
 color: var(--n-item-icon-color);
 transition:
 color .3s var(--n-bezier),
 font-size .3s var(--n-bezier),
 margin-right .3s var(--n-bezier);
 box-sizing: content-box;
 display: inline-flex;
 align-items: center;
 justify-content: center;
 `),p("arrow",`
 grid-area: arrow;
 font-size: 16px;
 color: var(--n-arrow-color);
 transform: rotate(180deg);
 opacity: 1;
 transition:
 color .3s var(--n-bezier),
 transform 0.2s var(--n-bezier),
 opacity 0.2s var(--n-bezier);
 `),m("menu-item-content-header",`
 grid-area: content;
 transition:
 color .3s var(--n-bezier),
 opacity .3s var(--n-bezier);
 opacity: 1;
 white-space: nowrap;
 color: var(--n-item-text-color);
 `,[g("a",`
 outline: none;
 text-decoration: none;
 transition: color .3s var(--n-bezier);
 color: var(--n-item-text-color);
 `,[g("&::before",`
 content: "";
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 `)]),p("extra",`
 font-size: .93em;
 color: var(--n-group-text-color);
 transition: color .3s var(--n-bezier);
 `)])]),m("submenu",`
 cursor: pointer;
 position: relative;
 margin-top: 6px;
 `,[m("menu-item-content",`
 height: var(--n-item-height);
 `),m("submenu-children",`
 overflow: hidden;
 padding: 0;
 `,[jo({duration:".2s"})])]),m("menu-item-group",[m("menu-item-group-title",`
 margin-top: 6px;
 color: var(--n-group-text-color);
 cursor: default;
 font-size: .93em;
 height: 36px;
 display: flex;
 align-items: center;
 transition:
 padding-left .3s var(--n-bezier),
 color .3s var(--n-bezier);
 `)])]),m("menu-tooltip",[g("a",`
 color: inherit;
 text-decoration: none;
 `)]),m("menu-divider",`
 transition: background-color .3s var(--n-bezier);
 background-color: var(--n-divider-color);
 height: 1px;
 margin: 6px 18px;
 `)]);function Q(e,t){return[A("hover",e,t),g("&:hover",e,t)]}const mo=N({name:"MenuOptionContent",props:{collapsed:Boolean,disabled:Boolean,title:[String,Function],icon:Function,extra:[String,Function],showArrow:Boolean,childActive:Boolean,hover:Boolean,paddingLeft:Number,selected:Boolean,maxIconSize:{type:Number,required:!0},activeIconSize:{type:Number,required:!0},iconMarginRight:{type:Number,required:!0},clsPrefix:{type:String,required:!0},onClick:Function,tmNode:{type:Object,required:!0},isEllipsisPlaceholder:Boolean},setup(e){const{props:t}=q(ue);return{menuProps:t,style:C(()=>{const{paddingLeft:o}=e;return{paddingLeft:o&&`${o}px`}}),iconStyle:C(()=>{const{maxIconSize:o,activeIconSize:n,iconMarginRight:l}=e;return{width:`${o}px`,height:`${o}px`,fontSize:`${n}px`,marginRight:`${l}px`}})}},render(){const{clsPrefix:e,tmNode:t,menuProps:{renderIcon:o,renderLabel:n,renderExtra:l,expandIcon:r}}=this,s=o?o(t.rawNode):le(this.icon);return a("div",{onClick:u=>{var d;(d=this.onClick)===null||d===void 0||d.call(this,u)},role:"none",class:[`${e}-menu-item-content`,{[`${e}-menu-item-content--selected`]:this.selected,[`${e}-menu-item-content--collapsed`]:this.collapsed,[`${e}-menu-item-content--child-active`]:this.childActive,[`${e}-menu-item-content--disabled`]:this.disabled,[`${e}-menu-item-content--hover`]:this.hover}],style:this.style},s&&a("div",{class:`${e}-menu-item-content__icon`,style:this.iconStyle,role:"none"},[s]),a("div",{class:`${e}-menu-item-content-header`,role:"none"},this.isEllipsisPlaceholder?this.title:n?n(t.rawNode):le(this.title),this.extra||l?a("span",{class:`${e}-menu-item-content-header__extra`}," ",l?l(t.rawNode):le(this.extra)):null),this.showArrow?a(no,{ariaHidden:!0,class:`${e}-menu-item-content__arrow`,clsPrefix:e},{default:()=>r?r(t.rawNode):a(vt,null)}):null)}}),fe=8;function $e(e){const t=q(ue),{props:o,mergedCollapsedRef:n}=t,l=q(vo,null),r=q(Te,null),s=C(()=>o.mode==="horizontal"),u=C(()=>s.value?o.dropdownPlacement:"tmNodes"in e?"right-start":"right"),d=C(()=>{var h;return Math.max((h=o.collapsedIconSize)!==null&&h!==void 0?h:o.iconSize,o.iconSize)}),v=C(()=>{var h;return!s.value&&e.root&&n.value&&(h=o.collapsedIconSize)!==null&&h!==void 0?h:o.iconSize}),b=C(()=>{if(s.value)return;const{collapsedWidth:h,indent:L,rootIndent:k}=o,{root:w,isGroup:R}=e,_=k===void 0?L:k;return w?n.value?h/2-d.value/2:_:r&&typeof r.paddingLeftRef.value=="number"?L/2+r.paddingLeftRef.value:l&&typeof l.paddingLeftRef.value=="number"?(R?L/2:L)+l.paddingLeftRef.value:0}),z=C(()=>{const{collapsedWidth:h,indent:L,rootIndent:k}=o,{value:w}=d,{root:R}=e;return s.value||!R||!n.value?fe:(k===void 0?L:k)+w+fe-(h+w)/2});return{dropdownPlacement:u,activeIconSize:v,maxIconSize:d,paddingLeft:b,iconMarginRight:z,NMenu:t,NSubmenu:l,NMenuOptionGroup:r}}const Ne={internalKey:{type:[String,Number],required:!0},root:Boolean,isGroup:Boolean,level:{type:Number,required:!0},title:[String,Function],extra:[String,Function]},Jt=N({name:"MenuDivider",setup(){const e=q(ue),{mergedClsPrefixRef:t,isHorizontalRef:o}=e;return()=>o.value?null:a("div",{class:`${t.value}-menu-divider`})}}),ho=Object.assign(Object.assign({},Ne),{tmNode:{type:Object,required:!0},disabled:Boolean,icon:Function,onClick:Function}),Qt=Oe(ho),er=N({name:"MenuOption",props:ho,setup(e){const t=$e(e),{NSubmenu:o,NMenu:n,NMenuOptionGroup:l}=t,{props:r,mergedClsPrefixRef:s,mergedCollapsedRef:u}=n,d=o?o.mergedDisabledRef:l?l.mergedDisabledRef:{value:!1},v=C(()=>d.value||e.disabled);function b(h){const{onClick:L}=e;L&&L(h)}function z(h){v.value||(n.doSelect(e.internalKey,e.tmNode.rawNode),b(h))}return{mergedClsPrefix:s,dropdownPlacement:t.dropdownPlacement,paddingLeft:t.paddingLeft,iconMarginRight:t.iconMarginRight,maxIconSize:t.maxIconSize,activeIconSize:t.activeIconSize,mergedTheme:n.mergedThemeRef,menuProps:r,dropdownEnabled:Se(()=>e.root&&u.value&&r.mode!=="horizontal"&&!v.value),selected:Se(()=>n.mergedValueRef.value===e.internalKey),mergedDisabled:v,handleClick:z}},render(){const{mergedClsPrefix:e,mergedTheme:t,tmNode:o,menuProps:{renderLabel:n,nodeProps:l}}=this,r=l==null?void 0:l(o.rawNode);return a("div",Object.assign({},r,{role:"menuitem",class:[`${e}-menu-item`,r==null?void 0:r.class]}),a(tt,{theme:t.peers.Tooltip,themeOverrides:t.peerOverrides.Tooltip,trigger:"hover",placement:this.dropdownPlacement,disabled:!this.dropdownEnabled||this.title===void 0,internalExtraClass:["menu-tooltip"]},{default:()=>n?n(o.rawNode):le(this.title),trigger:()=>a(mo,{tmNode:o,clsPrefix:e,paddingLeft:this.paddingLeft,iconMarginRight:this.iconMarginRight,maxIconSize:this.maxIconSize,activeIconSize:this.activeIconSize,selected:this.selected,title:this.title,extra:this.extra,disabled:this.mergedDisabled,icon:this.icon,onClick:this.handleClick})}))}}),fo=Object.assign(Object.assign({},Ne),{tmNode:{type:Object,required:!0},tmNodes:{type:Array,required:!0}}),or=Oe(fo),tr=N({name:"MenuOptionGroup",props:fo,setup(e){const t=$e(e),{NSubmenu:o}=t,n=C(()=>o!=null&&o.mergedDisabledRef.value?!0:e.tmNode.disabled);ee(Te,{paddingLeftRef:t.paddingLeft,mergedDisabledRef:n});const{mergedClsPrefixRef:l,props:r}=q(ue);return function(){const{value:s}=l,u=t.paddingLeft.value,{nodeProps:d}=r,v=d==null?void 0:d(e.tmNode.rawNode);return a("div",{class:`${s}-menu-item-group`,role:"group"},a("div",Object.assign({},v,{class:[`${s}-menu-item-group-title`,v==null?void 0:v.class],style:[(v==null?void 0:v.style)||"",u!==void 0?`padding-left: ${u}px;`:""]}),le(e.title),e.extra?a(lo,null," ",le(e.extra)):null),a("div",null,e.tmNodes.map(b=>Be(b,r))))}}});function He(e){return e.type==="divider"||e.type==="render"}function rr(e){return e.type==="divider"}function Be(e,t){const{rawNode:o}=e,{show:n}=o;if(n===!1)return null;if(He(o))return rr(o)?a(Jt,Object.assign({key:e.key},o.props)):null;const{labelField:l}=t,{key:r,level:s,isGroup:u}=e,d=Object.assign(Object.assign({},o),{title:o.title||o[l],extra:o.titleExtra||o.extra,key:r,internalKey:r,level:s,root:s===0,isGroup:u});return e.children?e.isGroup?a(tr,be(d,or,{tmNode:e,tmNodes:e.children,key:r})):a(ke,be(d,nr,{key:r,rawNodes:o[t.childrenField],tmNodes:e.children,tmNode:e})):a(er,be(d,Qt,{key:r,tmNode:e}))}const po=Object.assign(Object.assign({},Ne),{rawNodes:{type:Array,default:()=>[]},tmNodes:{type:Array,default:()=>[]},tmNode:{type:Object,required:!0},disabled:Boolean,icon:Function,onClick:Function,domId:String,virtualChildActive:{type:Boolean,default:void 0},isEllipsisPlaceholder:Boolean}),nr=Oe(po),ke=N({name:"Submenu",props:po,setup(e){const t=$e(e),{NMenu:o,NSubmenu:n}=t,{props:l,mergedCollapsedRef:r,mergedThemeRef:s}=o,u=C(()=>{const{disabled:h}=e;return n!=null&&n.mergedDisabledRef.value||l.disabled?!0:h}),d=M(!1);ee(vo,{paddingLeftRef:t.paddingLeft,mergedDisabledRef:u}),ee(Te,null);function v(){const{onClick:h}=e;h&&h()}function b(){u.value||(r.value||o.toggleExpand(e.internalKey),v())}function z(h){d.value=h}return{menuProps:l,mergedTheme:s,doSelect:o.doSelect,inverted:o.invertedRef,isHorizontal:o.isHorizontalRef,mergedClsPrefix:o.mergedClsPrefixRef,maxIconSize:t.maxIconSize,activeIconSize:t.activeIconSize,iconMarginRight:t.iconMarginRight,dropdownPlacement:t.dropdownPlacement,dropdownShow:d,paddingLeft:t.paddingLeft,mergedDisabled:u,mergedValue:o.mergedValueRef,childActive:Se(()=>{var h;return(h=e.virtualChildActive)!==null&&h!==void 0?h:o.activePathRef.value.includes(e.internalKey)}),collapsed:C(()=>l.mode==="horizontal"?!1:r.value?!0:!o.mergedExpandedKeysRef.value.includes(e.internalKey)),dropdownEnabled:C(()=>!u.value&&(l.mode==="horizontal"||r.value)),handlePopoverShowChange:z,handleClick:b}},render(){var e;const{mergedClsPrefix:t,menuProps:{renderIcon:o,renderLabel:n}}=this,l=()=>{const{isHorizontal:s,paddingLeft:u,collapsed:d,mergedDisabled:v,maxIconSize:b,activeIconSize:z,title:h,childActive:L,icon:k,handleClick:w,menuProps:{nodeProps:R},dropdownShow:_,iconMarginRight:x,tmNode:P,mergedClsPrefix:B,isEllipsisPlaceholder:y,extra:f}=this,S=R==null?void 0:R(P.rawNode);return a("div",Object.assign({},S,{class:[`${B}-menu-item`,S==null?void 0:S.class],role:"menuitem"}),a(mo,{tmNode:P,paddingLeft:u,collapsed:d,disabled:v,iconMarginRight:x,maxIconSize:b,activeIconSize:z,title:h,extra:f,showArrow:!s,childActive:L,clsPrefix:B,icon:k,hover:_,onClick:w,isEllipsisPlaceholder:y}))},r=()=>a(Ze,null,{default:()=>{const{tmNodes:s,collapsed:u}=this;return u?null:a("div",{class:`${t}-submenu-children`,role:"menu"},s.map(d=>Be(d,this.menuProps)))}});return this.root?a(io,Object.assign({size:"large",trigger:"hover"},(e=this.menuProps)===null||e===void 0?void 0:e.dropdownProps,{themeOverrides:this.mergedTheme.peerOverrides.Dropdown,theme:this.mergedTheme.peers.Dropdown,builtinThemeOverrides:{fontSizeLarge:"14px",optionIconSizeLarge:"18px"},value:this.mergedValue,disabled:!this.dropdownEnabled,placement:this.dropdownPlacement,keyField:this.menuProps.keyField,labelField:this.menuProps.labelField,childrenField:this.menuProps.childrenField,onUpdateShow:this.handlePopoverShowChange,options:this.rawNodes,onSelect:this.doSelect,inverted:this.inverted,renderIcon:o,renderLabel:n}),{default:()=>a("div",{class:`${t}-submenu`,role:"menu","aria-expanded":!this.collapsed,id:this.domId},l(),this.isHorizontal?null:r())}):a("div",{class:`${t}-submenu`,role:"menu","aria-expanded":!this.collapsed,id:this.domId},l(),r())}}),lr=Object.assign(Object.assign({},W.props),{options:{type:Array,default:()=>[]},collapsed:{type:Boolean,default:void 0},collapsedWidth:{type:Number,default:48},iconSize:{type:Number,default:20},collapsedIconSize:{type:Number,default:24},rootIndent:Number,indent:{type:Number,default:32},labelField:{type:String,default:"label"},keyField:{type:String,default:"key"},childrenField:{type:String,default:"children"},disabledField:{type:String,default:"disabled"},defaultExpandAll:Boolean,defaultExpandedKeys:Array,expandedKeys:Array,value:[String,Number],defaultValue:{type:[String,Number],default:null},mode:{type:String,default:"vertical"},watchProps:{type:Array,default:void 0},disabled:Boolean,show:{type:Boolean,default:!0},inverted:Boolean,"onUpdate:expandedKeys":[Function,Array],onUpdateExpandedKeys:[Function,Array],onUpdateValue:[Function,Array],"onUpdate:value":[Function,Array],expandIcon:Function,renderIcon:Function,renderLabel:Function,renderExtra:Function,dropdownProps:Object,accordion:Boolean,nodeProps:Function,dropdownPlacement:{type:String,default:"bottom"},responsive:Boolean,items:Array,onOpenNamesChange:[Function,Array],onSelect:[Function,Array],onExpandedNamesChange:[Function,Array],expandedNames:Array,defaultExpandedNames:Array}),ir=N({name:"Menu",inheritAttrs:!1,props:lr,setup(e){const{mergedClsPrefixRef:t,inlineThemeDisabled:o}=te(e),n=W("Menu","-menu",Zt,Et,e,t),l=q(so,null),r=C(()=>{var I;const{collapsed:T}=e;if(T!==void 0)return T;if(l){const{collapseModeRef:i,collapsedRef:H}=l;if(i.value==="width")return(I=H.value)!==null&&I!==void 0?I:!1}return!1}),s=C(()=>{const{keyField:I,childrenField:T,disabledField:i}=e;return ze(e.items||e.options,{getIgnored(H){return He(H)},getChildren(H){return H[T]},getDisabled(H){return H[i]},getKey(H){var F;return(F=H[I])!==null&&F!==void 0?F:H.name}})}),u=C(()=>new Set(s.value.treeNodes.map(I=>I.key))),{watchProps:d}=e,v=M(null);d!=null&&d.includes("defaultValue")?Ie(()=>{v.value=e.defaultValue}):v.value=e.defaultValue;const b=J(e,"value"),z=Re(b,v),h=M([]),L=()=>{h.value=e.defaultExpandAll?s.value.getNonLeafKeys():e.defaultExpandedNames||e.defaultExpandedKeys||s.value.getPath(z.value,{includeSelf:!1}).keyPath};d!=null&&d.includes("defaultExpandedKeys")?Ie(L):L();const k=it(e,["expandedNames","expandedKeys"]),w=Re(k,h),R=C(()=>s.value.treeNodes),_=C(()=>s.value.getPath(z.value).keyPath);ee(ue,{props:e,mergedCollapsedRef:r,mergedThemeRef:n,mergedValueRef:z,mergedExpandedKeysRef:w,activePathRef:_,mergedClsPrefixRef:t,isHorizontalRef:C(()=>e.mode==="horizontal"),invertedRef:J(e,"inverted"),doSelect:x,toggleExpand:B});function x(I,T){const{"onUpdate:value":i,onUpdateValue:H,onSelect:F}=e;H&&G(H,I,T),i&&G(i,I,T),F&&G(F,I,T),v.value=I}function P(I){const{"onUpdate:expandedKeys":T,onUpdateExpandedKeys:i,onExpandedNamesChange:H,onOpenNamesChange:F}=e;T&&G(T,I),i&&G(i,I),H&&G(H,I),F&&G(F,I),h.value=I}function B(I){const T=Array.from(w.value),i=T.findIndex(H=>H===I);if(~i)T.splice(i,1);else{if(e.accordion&&u.value.has(I)){const H=T.findIndex(F=>u.value.has(F));H>-1&&T.splice(H,1)}T.push(I)}P(T)}const y=I=>{const T=s.value.getPath(I??z.value,{includeSelf:!1}).keyPath;if(!T.length)return;const i=Array.from(w.value),H=new Set([...i,...T]);e.accordion&&u.value.forEach(F=>{H.has(F)&&!T.includes(F)&&H.delete(F)}),P(Array.from(H))},f=C(()=>{const{inverted:I}=e,{common:{cubicBezierEaseInOut:T},self:i}=n.value,{borderRadius:H,borderColorHorizontal:F,fontSize:zo,itemHeight:Io,dividerColor:So}=i,c={"--n-divider-color":So,"--n-bezier":T,"--n-font-size":zo,"--n-border-color-horizontal":F,"--n-border-radius":H,"--n-item-height":Io};return I?(c["--n-group-text-color"]=i.groupTextColorInverted,c["--n-color"]=i.colorInverted,c["--n-item-text-color"]=i.itemTextColorInverted,c["--n-item-text-color-hover"]=i.itemTextColorHoverInverted,c["--n-item-text-color-active"]=i.itemTextColorActiveInverted,c["--n-item-text-color-child-active"]=i.itemTextColorChildActiveInverted,c["--n-item-text-color-child-active-hover"]=i.itemTextColorChildActiveInverted,c["--n-item-text-color-active-hover"]=i.itemTextColorActiveHoverInverted,c["--n-item-icon-color"]=i.itemIconColorInverted,c["--n-item-icon-color-hover"]=i.itemIconColorHoverInverted,c["--n-item-icon-color-active"]=i.itemIconColorActiveInverted,c["--n-item-icon-color-active-hover"]=i.itemIconColorActiveHoverInverted,c["--n-item-icon-color-child-active"]=i.itemIconColorChildActiveInverted,c["--n-item-icon-color-child-active-hover"]=i.itemIconColorChildActiveHoverInverted,c["--n-item-icon-color-collapsed"]=i.itemIconColorCollapsedInverted,c["--n-item-text-color-horizontal"]=i.itemTextColorHorizontalInverted,c["--n-item-text-color-hover-horizontal"]=i.itemTextColorHoverHorizontalInverted,c["--n-item-text-color-active-horizontal"]=i.itemTextColorActiveHorizontalInverted,c["--n-item-text-color-child-active-horizontal"]=i.itemTextColorChildActiveHorizontalInverted,c["--n-item-text-color-child-active-hover-horizontal"]=i.itemTextColorChildActiveHoverHorizontalInverted,c["--n-item-text-color-active-hover-horizontal"]=i.itemTextColorActiveHoverHorizontalInverted,c["--n-item-icon-color-horizontal"]=i.itemIconColorHorizontalInverted,c["--n-item-icon-color-hover-horizontal"]=i.itemIconColorHoverHorizontalInverted,c["--n-item-icon-color-active-horizontal"]=i.itemIconColorActiveHorizontalInverted,c["--n-item-icon-color-active-hover-horizontal"]=i.itemIconColorActiveHoverHorizontalInverted,c["--n-item-icon-color-child-active-horizontal"]=i.itemIconColorChildActiveHorizontalInverted,c["--n-item-icon-color-child-active-hover-horizontal"]=i.itemIconColorChildActiveHoverHorizontalInverted,c["--n-arrow-color"]=i.arrowColorInverted,c["--n-arrow-color-hover"]=i.arrowColorHoverInverted,c["--n-arrow-color-active"]=i.arrowColorActiveInverted,c["--n-arrow-color-active-hover"]=i.arrowColorActiveHoverInverted,c["--n-arrow-color-child-active"]=i.arrowColorChildActiveInverted,c["--n-arrow-color-child-active-hover"]=i.arrowColorChildActiveHoverInverted,c["--n-item-color-hover"]=i.itemColorHoverInverted,c["--n-item-color-active"]=i.itemColorActiveInverted,c["--n-item-color-active-hover"]=i.itemColorActiveHoverInverted,c["--n-item-color-active-collapsed"]=i.itemColorActiveCollapsedInverted):(c["--n-group-text-color"]=i.groupTextColor,c["--n-color"]=i.color,c["--n-item-text-color"]=i.itemTextColor,c["--n-item-text-color-hover"]=i.itemTextColorHover,c["--n-item-text-color-active"]=i.itemTextColorActive,c["--n-item-text-color-child-active"]=i.itemTextColorChildActive,c["--n-item-text-color-child-active-hover"]=i.itemTextColorChildActiveHover,c["--n-item-text-color-active-hover"]=i.itemTextColorActiveHover,c["--n-item-icon-color"]=i.itemIconColor,c["--n-item-icon-color-hover"]=i.itemIconColorHover,c["--n-item-icon-color-active"]=i.itemIconColorActive,c["--n-item-icon-color-active-hover"]=i.itemIconColorActiveHover,c["--n-item-icon-color-child-active"]=i.itemIconColorChildActive,c["--n-item-icon-color-child-active-hover"]=i.itemIconColorChildActiveHover,c["--n-item-icon-color-collapsed"]=i.itemIconColorCollapsed,c["--n-item-text-color-horizontal"]=i.itemTextColorHorizontal,c["--n-item-text-color-hover-horizontal"]=i.itemTextColorHoverHorizontal,c["--n-item-text-color-active-horizontal"]=i.itemTextColorActiveHorizontal,c["--n-item-text-color-child-active-horizontal"]=i.itemTextColorChildActiveHorizontal,c["--n-item-text-color-child-active-hover-horizontal"]=i.itemTextColorChildActiveHoverHorizontal,c["--n-item-text-color-active-hover-horizontal"]=i.itemTextColorActiveHoverHorizontal,c["--n-item-icon-color-horizontal"]=i.itemIconColorHorizontal,c["--n-item-icon-color-hover-horizontal"]=i.itemIconColorHoverHorizontal,c["--n-item-icon-color-active-horizontal"]=i.itemIconColorActiveHorizontal,c["--n-item-icon-color-active-hover-horizontal"]=i.itemIconColorActiveHoverHorizontal,c["--n-item-icon-color-child-active-horizontal"]=i.itemIconColorChildActiveHorizontal,c["--n-item-icon-color-child-active-hover-horizontal"]=i.itemIconColorChildActiveHoverHorizontal,c["--n-arrow-color"]=i.arrowColor,c["--n-arrow-color-hover"]=i.arrowColorHover,c["--n-arrow-color-active"]=i.arrowColorActive,c["--n-arrow-color-active-hover"]=i.arrowColorActiveHover,c["--n-arrow-color-child-active"]=i.arrowColorChildActive,c["--n-arrow-color-child-active-hover"]=i.arrowColorChildActiveHover,c["--n-item-color-hover"]=i.itemColorHover,c["--n-item-color-active"]=i.itemColorActive,c["--n-item-color-active-hover"]=i.itemColorActiveHover,c["--n-item-color-active-collapsed"]=i.itemColorActiveCollapsed),c}),S=o?re("menu",C(()=>e.inverted?"a":"b"),f,e):void 0,E=Vo(),D=M(null),X=M(null);let U=!0;const ve=()=>{var I;U?U=!1:(I=D.value)===null||I===void 0||I.sync({showAllItemsBeforeCalculate:!0})};function ie(){return document.getElementById(E)}const me=M(-1);function go(I){me.value=e.options.length-I}function bo(I){I||(me.value=-1)}const xo=C(()=>{const I=me.value;return{children:I===-1?[]:e.options.slice(I)}}),Co=C(()=>{const{childrenField:I,disabledField:T,keyField:i}=e;return ze([xo.value],{getIgnored(H){return He(H)},getChildren(H){return H[I]},getDisabled(H){return H[T]},getKey(H){var F;return(F=H[i])!==null&&F!==void 0?F:H.name}})}),yo=C(()=>ze([{}]).treeNodes[0]);function wo(){var I;if(me.value===-1)return a(ke,{root:!0,level:0,key:"__ellpisisGroupPlaceholder__",internalKey:"__ellpisisGroupPlaceholder__",title:"···",tmNode:yo.value,domId:E,isEllipsisPlaceholder:!0});const T=Co.value.treeNodes[0],i=_.value,H=!!(!((I=T.children)===null||I===void 0)&&I.some(F=>i.includes(F.key)));return a(ke,{level:0,root:!0,key:"__ellpisisGroup__",internalKey:"__ellpisisGroup__",title:"···",virtualChildActive:H,tmNode:T,domId:E,rawNodes:T.rawNode.children||[],tmNodes:T.children||[],isEllipsisPlaceholder:!0})}return{mergedClsPrefix:t,controlledExpandedKeys:k,uncontrolledExpanededKeys:h,mergedExpandedKeys:w,uncontrolledValue:v,mergedValue:z,activePath:_,tmNodes:R,mergedTheme:n,mergedCollapsed:r,cssVars:o?void 0:f,themeClass:S==null?void 0:S.themeClass,overflowRef:D,counterRef:X,updateCounter:()=>{},onResize:ve,onUpdateOverflow:bo,onUpdateCount:go,renderCounter:wo,getCounter:ie,onRender:S==null?void 0:S.onRender,showOption:y,deriveResponsiveState:ve}},render(){const{mergedClsPrefix:e,mode:t,themeClass:o,onRender:n}=this;n==null||n();const l=()=>this.tmNodes.map(d=>Be(d,this.$props)),s=t==="horizontal"&&this.responsive,u=()=>a("div",Ko(this.$attrs,{role:t==="horizontal"?"menubar":"menu",class:[`${e}-menu`,o,`${e}-menu--${t}`,s&&`${e}-menu--responsive`,this.mergedCollapsed&&`${e}-menu--collapsed`],style:this.cssVars}),s?a(nt,{ref:"overflowRef",onUpdateOverflow:this.onUpdateOverflow,getCounter:this.getCounter,onUpdateCount:this.onUpdateCount,updateCounter:this.updateCounter,style:{width:"100%",display:"flex",overflow:"hidden"}},{default:l,counter:this.renderCounter}):l());return s?a(Je,{onResize:this.onResize},{default:u}):u()}}),ar={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 1024 1024"},sr=N({name:"BellOutlined",render:function(t,o){return j(),Y("svg",ar,o[0]||(o[0]=[O("path",{d:"M816 768h-24V428c0-141.1-104.3-257.7-240-277.1V112c0-22.1-17.9-40-40-40s-40 17.9-40 40v38.9c-135.7 19.4-240 136-240 277.1v340h-24c-17.7 0-32 14.3-32 32v32c0 4.4 3.6 8 8 8h216c0 61.8 50.2 112 112 112s112-50.2 112-112h216c4.4 0 8-3.6 8-8v-32c0-17.7-14.3-32-32-32zM512 888c-26.5 0-48-21.5-48-48h96c0 26.5-21.5 48-48 48zM304 768V428c0-55.6 21.6-107.8 60.9-147.1S456.4 220 512 220c55.6 0 107.8 21.6 147.1 60.9S720 372.4 720 428v340H304z",fill:"currentColor"},null,-1)]))}}),cr={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 1024 1024"},dr=N({name:"DashboardOutlined",render:function(t,o){return j(),Y("svg",cr,o[0]||(o[0]=[O("path",{d:"M924.8 385.6a446.7 446.7 0 0 0-96-142.4a446.7 446.7 0 0 0-142.4-96C631.1 123.8 572.5 112 512 112s-119.1 11.8-174.4 35.2a446.7 446.7 0 0 0-142.4 96a446.7 446.7 0 0 0-96 142.4C75.8 440.9 64 499.5 64 560c0 132.7 58.3 257.7 159.9 343.1l1.7 1.4c5.8 4.8 13.1 7.5 20.6 7.5h531.7c7.5 0 14.8-2.7 20.6-7.5l1.7-1.4C901.7 817.7 960 692.7 960 560c0-60.5-11.9-119.1-35.2-174.4zM761.4 836H262.6A371.12 371.12 0 0 1 140 560c0-99.4 38.7-192.8 109-263c70.3-70.3 163.7-109 263-109c99.4 0 192.8 38.7 263 109c70.3 70.3 109 163.7 109 263c0 105.6-44.5 205.5-122.6 276zM623.5 421.5a8.03 8.03 0 0 0-11.3 0L527.7 506c-18.7-5-39.4-.2-54.1 14.5a55.95 55.95 0 0 0 0 79.2a55.95 55.95 0 0 0 79.2 0a55.87 55.87 0 0 0 14.5-54.1l84.5-84.5c3.1-3.1 3.1-8.2 0-11.3l-28.3-28.3zM490 320h44c4.4 0 8-3.6 8-8v-80c0-4.4-3.6-8-8-8h-44c-4.4 0-8 3.6-8 8v80c0 4.4 3.6 8 8 8zm260 218v44c0 4.4 3.6 8 8 8h80c4.4 0 8-3.6 8-8v-44c0-4.4-3.6-8-8-8h-80c-4.4 0-8 3.6-8 8zm12.7-197.2l-31.1-31.1a8.03 8.03 0 0 0-11.3 0l-56.6 56.6a8.03 8.03 0 0 0 0 11.3l31.1 31.1c3.1 3.1 8.2 3.1 11.3 0l56.6-56.6c3.1-3.1 3.1-8.2 0-11.3zm-458.6-31.1a8.03 8.03 0 0 0-11.3 0l-31.1 31.1a8.03 8.03 0 0 0 0 11.3l56.6 56.6c3.1 3.1 8.2 3.1 11.3 0l31.1-31.1c3.1-3.1 3.1-8.2 0-11.3l-56.6-56.6zM262 530h-80c-4.4 0-8 3.6-8 8v44c0 4.4 3.6 8 8 8h80c4.4 0 8-3.6 8-8v-44c0-4.4-3.6-8-8-8z",fill:"currentColor"},null,-1)]))}}),ur={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 1024 1024"},qe=N({name:"FileSearchOutlined",render:function(t,o){return j(),Y("svg",ur,o[0]||(o[0]=[O("path",{d:"M688 312v-48c0-4.4-3.6-8-8-8H296c-4.4 0-8 3.6-8 8v48c0 4.4 3.6 8 8 8h384c4.4 0 8-3.6 8-8zm-392 88c-4.4 0-8 3.6-8 8v48c0 4.4 3.6 8 8 8h184c4.4 0 8-3.6 8-8v-48c0-4.4-3.6-8-8-8H296zm144 452H208V148h560v344c0 4.4 3.6 8 8 8h56c4.4 0 8-3.6 8-8V108c0-17.7-14.3-32-32-32H168c-17.7 0-32 14.3-32 32v784c0 17.7 14.3 32 32 32h272c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8zm445.7 51.5l-93.3-93.3C814.7 780.7 828 743.9 828 704c0-97.2-78.8-176-176-176s-176 78.8-176 176s78.8 176 176 176c35.8 0 69-10.7 96.8-29l94.7 94.7c1.6 1.6 3.6 2.3 5.6 2.3s4.1-.8 5.6-2.3l31-31a7.9 7.9 0 0 0 0-11.2zM652 816c-61.9 0-112-50.1-112-112s50.1-112 112-112s112 50.1 112 112s-50.1 112-112 112z",fill:"currentColor"},null,-1)]))}}),vr={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 1024 1024"},mr=N({name:"FolderOpenOutlined",render:function(t,o){return j(),Y("svg",vr,o[0]||(o[0]=[O("path",{d:"M928 444H820V330.4c0-17.7-14.3-32-32-32H473L355.7 186.2a8.15 8.15 0 0 0-5.5-2.2H96c-17.7 0-32 14.3-32 32v592c0 17.7 14.3 32 32 32h698c13 0 24.8-7.9 29.7-20l134-332c1.5-3.8 2.3-7.9 2.3-12c0-17.7-14.3-32-32-32zM136 256h188.5l119.6 114.4H748V444H238c-13 0-24.8 7.9-29.7 20L136 643.2V256zm635.3 512H159l103.3-256h612.4L771.3 768z",fill:"currentColor"},null,-1)]))}}),hr={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 1024 1024"},fr=N({name:"FullscreenExitOutlined",render:function(t,o){return j(),Y("svg",hr,o[0]||(o[0]=[O("path",{d:"M391 240.9c-.8-6.6-8.9-9.4-13.6-4.7l-43.7 43.7L200 146.3a8.03 8.03 0 0 0-11.3 0l-42.4 42.3a8.03 8.03 0 0 0 0 11.3L280 333.6l-43.9 43.9a8.01 8.01 0 0 0 4.7 13.6L401 410c5.1.6 9.5-3.7 8.9-8.9L391 240.9zm10.1 373.2L240.8 633c-6.6.8-9.4 8.9-4.7 13.6l43.9 43.9L146.3 824a8.03 8.03 0 0 0 0 11.3l42.4 42.3c3.1 3.1 8.2 3.1 11.3 0L333.7 744l43.7 43.7A8.01 8.01 0 0 0 391 783l18.9-160.1c.6-5.1-3.7-9.4-8.8-8.8zm221.8-204.2L783.2 391c6.6-.8 9.4-8.9 4.7-13.6L744 333.6L877.7 200c3.1-3.1 3.1-8.2 0-11.3l-42.4-42.3a8.03 8.03 0 0 0-11.3 0L690.3 279.9l-43.7-43.7a8.01 8.01 0 0 0-13.6 4.7L614.1 401c-.6 5.2 3.7 9.5 8.8 8.9zM744 690.4l43.9-43.9a8.01 8.01 0 0 0-4.7-13.6L623 614c-5.1-.6-9.5 3.7-8.9 8.9L633 783.1c.8 6.6 8.9 9.4 13.6 4.7l43.7-43.7L824 877.7c3.1 3.1 8.2 3.1 11.3 0l42.4-42.3c3.1-3.1 3.1-8.2 0-11.3L744 690.4z",fill:"currentColor"},null,-1)]))}}),pr={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 1024 1024"},gr=N({name:"FullscreenOutlined",render:function(t,o){return j(),Y("svg",pr,o[0]||(o[0]=[O("path",{d:"M290 236.4l43.9-43.9a8.01 8.01 0 0 0-4.7-13.6L169 160c-5.1-.6-9.5 3.7-8.9 8.9L179 329.1c.8 6.6 8.9 9.4 13.6 4.7l43.7-43.7L370 423.7c3.1 3.1 8.2 3.1 11.3 0l42.4-42.3c3.1-3.1 3.1-8.2 0-11.3L290 236.4zm352.7 187.3c3.1 3.1 8.2 3.1 11.3 0l133.7-133.6l43.7 43.7a8.01 8.01 0 0 0 13.6-4.7L863.9 169c.6-5.1-3.7-9.5-8.9-8.9L694.8 179c-6.6.8-9.4 8.9-4.7 13.6l43.9 43.9L600.3 370a8.03 8.03 0 0 0 0 11.3l42.4 42.4zM845 694.9c-.8-6.6-8.9-9.4-13.6-4.7l-43.7 43.7L654 600.3a8.03 8.03 0 0 0-11.3 0l-42.4 42.3a8.03 8.03 0 0 0 0 11.3L734 787.6l-43.9 43.9a8.01 8.01 0 0 0 4.7 13.6L855 864c5.1.6 9.5-3.7 8.9-8.9L845 694.9zm-463.7-94.6a8.03 8.03 0 0 0-11.3 0L236.3 733.9l-43.7-43.7a8.01 8.01 0 0 0-13.6 4.7L160.1 855c-.6 5.1 3.7 9.5 8.9 8.9L329.2 845c6.6-.8 9.4-8.9 4.7-13.6L290 787.6L423.7 654c3.1-3.1 3.1-8.2 0-11.3l-42.4-42.4z",fill:"currentColor"},null,-1)]))}}),br={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 1024 1024"},xr=N({name:"HomeOutlined",render:function(t,o){return j(),Y("svg",br,o[0]||(o[0]=[O("path",{d:"M946.5 505L560.1 118.8l-25.9-25.9a31.5 31.5 0 0 0-44.4 0L77.5 505a63.9 63.9 0 0 0-18.8 46c.4 35.2 29.7 63.3 64.9 63.3h42.5V940h691.8V614.3h43.4c17.1 0 33.2-6.7 45.3-18.8a63.6 63.6 0 0 0 18.7-45.3c0-17-6.7-33.1-18.8-45.2zM568 868H456V664h112v204zm217.9-325.7V868H632V640c0-22.1-17.9-40-40-40H432c-22.1 0-40 17.9-40 40v228H238.1V542.3h-96l370-369.7l23.1 23.1L882 542.3h-96.1z",fill:"currentColor"},null,-1)]))}}),Cr={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 1024 1024"},Xe=N({name:"LogoutOutlined",render:function(t,o){return j(),Y("svg",Cr,o[0]||(o[0]=[O("path",{d:"M868 732h-70.3c-4.8 0-9.3 2.1-12.3 5.8c-7 8.5-14.5 16.7-22.4 24.5a353.84 353.84 0 0 1-112.7 75.9A352.8 352.8 0 0 1 512.4 866c-47.9 0-94.3-9.4-137.9-27.8a353.84 353.84 0 0 1-112.7-75.9a353.28 353.28 0 0 1-76-112.5C167.3 606.2 158 559.9 158 512s9.4-94.2 27.8-137.8c17.8-42.1 43.4-80 76-112.5s70.5-58.1 112.7-75.9c43.6-18.4 90-27.8 137.9-27.8c47.9 0 94.3 9.3 137.9 27.8c42.2 17.8 80.1 43.4 112.7 75.9c7.9 7.9 15.3 16.1 22.4 24.5c3 3.7 7.6 5.8 12.3 5.8H868c6.3 0 10.2-7 6.7-12.3C798 160.5 663.8 81.6 511.3 82C271.7 82.6 79.6 277.1 82 516.4C84.4 751.9 276.2 942 512.4 942c152.1 0 285.7-78.8 362.3-197.7c3.4-5.3-.4-12.3-6.7-12.3zm88.9-226.3L815 393.7c-5.3-4.2-13-.4-13 6.3v76H488c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8h314v76c0 6.7 7.8 10.5 13 6.3l141.9-112a8 8 0 0 0 0-12.6z",fill:"currentColor"},null,-1)]))}}),yr={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 1024 1024"},wr=N({name:"MenuFoldOutlined",render:function(t,o){return j(),Y("svg",yr,o[0]||(o[0]=[O("path",{d:"M408 442h480c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8H408c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8zm-8 204c0 4.4 3.6 8 8 8h480c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8H408c-4.4 0-8 3.6-8 8v56zm504-486H120c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8zm0 632H120c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8zM115.4 518.9L271.7 642c5.8 4.6 14.4.5 14.4-6.9V388.9c0-7.4-8.5-11.5-14.4-6.9L115.4 505.1a8.74 8.74 0 0 0 0 13.8z",fill:"currentColor"},null,-1)]))}}),zr={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 1024 1024"},Ir=N({name:"MenuUnfoldOutlined",render:function(t,o){return j(),Y("svg",zr,o[0]||(o[0]=[O("path",{d:"M408 442h480c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8H408c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8zm-8 204c0 4.4 3.6 8 8 8h480c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8H408c-4.4 0-8 3.6-8 8v56zm504-486H120c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8zm0 632H120c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-56c0-4.4-3.6-8-8-8zM142.4 642.1L298.7 519a8.84 8.84 0 0 0 0-13.9L142.4 381.9c-5.8-4.6-14.4-.5-14.4 6.9v246.3a8.9 8.9 0 0 0 14.4 7z",fill:"currentColor"},null,-1)]))}}),Sr={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 1024 1024"},Rr=N({name:"SettingOutlined",render:function(t,o){return j(),Y("svg",Sr,o[0]||(o[0]=[O("path",{d:"M924.8 625.7l-65.5-56c3.1-19 4.7-38.4 4.7-57.8s-1.6-38.8-4.7-57.8l65.5-56a32.03 32.03 0 0 0 9.3-35.2l-.9-2.6a443.74 443.74 0 0 0-79.7-137.9l-1.8-2.1a32.12 32.12 0 0 0-35.1-9.5l-81.3 28.9c-30-24.6-63.5-44-99.7-57.6l-15.7-85a32.05 32.05 0 0 0-25.8-25.7l-2.7-.5c-52.1-9.4-106.9-9.4-159 0l-2.7.5a32.05 32.05 0 0 0-25.8 25.7l-15.8 85.4a351.86 351.86 0 0 0-99 57.4l-81.9-29.1a32 32 0 0 0-35.1 9.5l-1.8 2.1a446.02 446.02 0 0 0-79.7 137.9l-.9 2.6c-4.5 12.5-.8 26.5 9.3 35.2l66.3 56.6c-3.1 18.8-4.6 38-4.6 57.1c0 19.2 1.5 38.4 4.6 57.1L99 625.5a32.03 32.03 0 0 0-9.3 35.2l.9 2.6c18.1 50.4 44.9 96.9 79.7 137.9l1.8 2.1a32.12 32.12 0 0 0 35.1 9.5l81.9-29.1c29.8 24.5 63.1 43.9 99 57.4l15.8 85.4a32.05 32.05 0 0 0 25.8 25.7l2.7.5a449.4 449.4 0 0 0 159 0l2.7-.5a32.05 32.05 0 0 0 25.8-25.7l15.7-85a350 350 0 0 0 99.7-57.6l81.3 28.9a32 32 0 0 0 35.1-9.5l1.8-2.1c34.8-41.1 61.6-87.5 79.7-137.9l.9-2.6c4.5-12.3.8-26.3-9.3-35zM788.3 465.9c2.5 15.1 3.8 30.6 3.8 46.1s-1.3 31-3.8 46.1l-6.6 40.1l74.7 63.9a370.03 370.03 0 0 1-42.6 73.6L721 702.8l-31.4 25.8c-23.9 19.6-50.5 35-79.3 45.8l-38.1 14.3l-17.9 97a377.5 377.5 0 0 1-85 0l-17.9-97.2l-37.8-14.5c-28.5-10.8-55-26.2-78.7-45.7l-31.4-25.9l-93.4 33.2c-17-22.9-31.2-47.6-42.6-73.6l75.5-64.5l-6.5-40c-2.4-14.9-3.7-30.3-3.7-45.5c0-15.3 1.2-30.6 3.7-45.5l6.5-40l-75.5-64.5c11.3-26.1 25.6-50.7 42.6-73.6l93.4 33.2l31.4-25.9c23.7-19.5 50.2-34.9 78.7-45.7l37.9-14.3l17.9-97.2c28.1-3.2 56.8-3.2 85 0l17.9 97l38.1 14.3c28.7 10.8 55.4 26.2 79.3 45.8l31.4 25.8l92.8-32.9c17 22.9 31.2 47.6 42.6 73.6L781.8 426l6.5 39.9zM512 326c-97.2 0-176 78.8-176 176s78.8 176 176 176s176-78.8 176-176s-78.8-176-176-176zm79.2 255.2A111.6 111.6 0 0 1 512 614c-29.9 0-58-11.7-79.2-32.8A111.6 111.6 0 0 1 400 502c0-29.9 11.7-58 32.8-79.2C454 401.6 482.1 390 512 390c29.9 0 58 11.6 79.2 32.8A111.6 111.6 0 0 1 624 502c0 29.9-11.7 58-32.8 79.2z",fill:"currentColor"},null,-1)]))}}),Hr={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 1024 1024"},kr=N({name:"ShareAltOutlined",render:function(t,o){return j(),Y("svg",Hr,o[0]||(o[0]=[O("path",{d:"M752 664c-28.5 0-54.8 10-75.4 26.7L469.4 540.8a160.68 160.68 0 0 0 0-57.6l207.2-149.9C697.2 350 723.5 360 752 360c66.2 0 120-53.8 120-120s-53.8-120-120-120s-120 53.8-120 120c0 11.6 1.6 22.7 4.7 33.3L439.9 415.8C410.7 377.1 364.3 352 312 352c-88.4 0-160 71.6-160 160s71.6 160 160 160c52.3 0 98.7-25.1 127.9-63.8l196.8 142.5c-3.1 10.6-4.7 21.8-4.7 33.3c0 66.2 53.8 120 120 120s120-53.8 120-120s-53.8-120-120-120zm0-476c28.7 0 52 23.3 52 52s-23.3 52-52 52s-52-23.3-52-52s23.3-52 52-52zM312 600c-48.5 0-88-39.5-88-88s39.5-88 88-88s88 39.5 88 88s-39.5 88-88 88zm440 236c-28.7 0-52-23.3-52-52s23.3-52 52-52s52 23.3 52 52s-23.3 52-52 52z",fill:"currentColor"},null,-1)]))}}),Ar={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 1024 1024"},Pr=N({name:"TeamOutlined",render:function(t,o){return j(),Y("svg",Ar,o[0]||(o[0]=[O("path",{d:"M824.2 699.9a301.55 301.55 0 0 0-86.4-60.4C783.1 602.8 812 546.8 812 484c0-110.8-92.4-201.7-203.2-200c-109.1 1.7-197 90.6-197 200c0 62.8 29 118.8 74.2 155.5a300.95 300.95 0 0 0-86.4 60.4C345 754.6 314 826.8 312 903.8a8 8 0 0 0 8 8.2h56c4.3 0 7.9-3.4 8-7.7c1.9-58 25.4-112.3 66.7-153.5A226.62 226.62 0 0 1 612 684c60.9 0 118.2 23.7 161.3 66.8C814.5 792 838 846.3 840 904.3c.1 4.3 3.7 7.7 8 7.7h56a8 8 0 0 0 8-8.2c-2-77-33-149.2-87.8-203.9zM612 612c-34.2 0-66.4-13.3-90.5-37.5a126.86 126.86 0 0 1-37.5-91.8c.3-32.8 13.4-64.5 36.3-88c24-24.6 56.1-38.3 90.4-38.7c33.9-.3 66.8 12.9 91 36.6c24.8 24.3 38.4 56.8 38.4 91.4c0 34.2-13.3 66.3-37.5 90.5A127.3 127.3 0 0 1 612 612zM361.5 510.4c-.9-8.7-1.4-17.5-1.4-26.4c0-15.9 1.5-31.4 4.3-46.5c.7-3.6-1.2-7.3-4.5-8.8c-13.6-6.1-26.1-14.5-36.9-25.1a127.54 127.54 0 0 1-38.7-95.4c.9-32.1 13.8-62.6 36.3-85.6c24.7-25.3 57.9-39.1 93.2-38.7c31.9.3 62.7 12.6 86 34.4c7.9 7.4 14.7 15.6 20.4 24.4c2 3.1 5.9 4.4 9.3 3.2c17.6-6.1 36.2-10.4 55.3-12.4c5.6-.6 8.8-6.6 6.3-11.6c-32.5-64.3-98.9-108.7-175.7-109.9c-110.9-1.7-203.3 89.2-203.3 199.9c0 62.8 28.9 118.8 74.2 155.5c-31.8 14.7-61.1 35-86.5 60.4c-54.8 54.7-85.8 126.9-87.8 204a8 8 0 0 0 8 8.2h56.1c4.3 0 7.9-3.4 8-7.7c1.9-58 25.4-112.3 66.7-153.5c29.4-29.4 65.4-49.8 104.7-59.7c3.9-1 6.5-4.7 6-8.7z",fill:"currentColor"},null,-1)]))}}),Or={class:"logo-area"},Lr={class:"logo-text"},_r={class:"menu-wrapper"},Tr={class:"sider-footer"},$r={class:"header-left"},Nr={key:0,class:"breadcrumb-area"},Br={class:"header-right"},Mr={class:"user-info"},Er={class:"user-detail"},Fr={class:"user-name"},jr={class:"user-role"},Vr={class:"page-container"},Kr={__name:"AdminLayout",setup(e){const t=Yo(),o=Uo(),n=Do(),l=et(),r=M(!1),s=M(!1),u=M(0),d=C(()=>{const y=[{label:"仪表盘",key:"/dashboard",icon:()=>a(dr)},{label:"内容管理",key:"/content",icon:()=>a(Ke),children:[{label:"文章管理",key:"/articles",icon:()=>a(Ke)},{label:"策展队列",key:"/articles/review",icon:()=>a(Ve)},{label:"工具管理",key:"/tools",icon:()=>a(ut)}]},{label:"分类管理",key:"/categories",icon:()=>a(mr)},{label:"标签管理",key:"/tags",icon:()=>a(dt)},{label:"来源管理",key:"/sources",icon:()=>a(kr)},{label:"运营",key:"/ops",icon:()=>a(De),children:[{label:"采集监控",key:"/crawler-monitor",icon:()=>a(De)},{label:"每日观察报告",key:"/observation-report",icon:()=>a(qe)}]}];return n.isSuperAdmin&&y.push({label:"系统管理",key:"/system",icon:()=>a(Rr),children:[{label:"管理员管理",key:"/system/admins",icon:()=>a(Pr)},{label:"角色权限",key:"/system/roles",icon:()=>a(Ve)},{label:"审计日志",key:"/system/audit-logs",icon:()=>a(qe)}]}),y}),v=[{label:"个人信息",key:"profile",icon:()=>a(je)},{type:"divider",key:"d1"},{label:"退出登录",key:"logout",icon:()=>a(Xe)}],b=C(()=>o.meta.activeMenu?o.meta.activeMenu:o.path),z=M([]);function h(){const y=[];(o.path.startsWith("/articles")||o.path.startsWith("/tools"))&&y.push("/content"),(o.path.startsWith("/crawler-monitor")||o.path.startsWith("/observation-report"))&&y.push("/ops"),o.path.startsWith("/system/")&&y.push("/system"),z.value=y}h(),pe(()=>o.path,h);function L(y){z.value=y}const k=C(()=>{const y=[],f=o.matched.filter(S=>S.meta&&S.meta.title&&S.path!=="/");return f.length>0&&y.push({label:"首页",key:"/dashboard",icon:()=>a(xr),clickable:!0}),f.forEach((S,E)=>{y.push({label:S.meta.title,key:S.path,clickable:E<f.length-1})}),y});function w(y){t.push(y)}function R(y){y==="profile"?l.info("个人信息功能即将上线，当前可在「系统管理-管理员管理」查看账号信息"):y==="logout"&&_()}async function _(){await n.logout(),t.push("/login")}function x(){u.value===0?l.info("暂无新通知"):l.info(`您有 ${u.value} 条未读通知`)}function P(){r.value=!r.value}function B(){document.fullscreenElement?(document.exitFullscreen(),s.value=!1):(document.documentElement.requestFullscreen(),s.value=!0)}return(y,f)=>{const S=Wo("router-view");return j(),Z($(Ye),{"has-sider":"",class:"admin-layout"},{default:K(()=>[V($(Xt),{collapsed:r.value,"collapsed-width":64,width:240,"native-scrollbar":!1,"show-trigger":"bar",class:"layout-sider",onCollapse:f[0]||(f[0]=E=>r.value=!0),onExpand:f[1]||(f[1]=E=>r.value=!1)},{default:K(()=>[O("div",Or,[f[2]||(f[2]=O("div",{class:"logo-icon"},[O("svg",{viewBox:"0 0 32 32",fill:"none",xmlns:"http://www.w3.org/2000/svg"},[O("path",{d:"M16 2L26 8V24L16 30L6 24V8L16 2Z",fill:"#111827"}),O("circle",{cx:"16",cy:"16",r:"4",fill:"white",opacity:"0.9"})])],-1)),xe(O("div",Lr,"EntropyGate AI",512),[[Ce,!r.value]])]),O("div",_r,[V($(ir),{value:b.value,"expanded-keys":z.value,options:d.value,collapsed:r.value,"collapsed-width":64,indent:20,"onUpdate:value":w,"onUpdate:expandedKeys":L},null,8,["value","expanded-keys","options","collapsed"])]),xe(O("div",Tr,[...f[3]||(f[3]=[O("div",{class:"version-info"},[O("span",{class:"version-label"},"版本"),O("span",{class:"version-num"},"v1.0.0")],-1)])],512),[[Ce,!r.value]])]),_:1},8,["collapsed"]),V($(Ye),{class:"main-layout"},{default:K(()=>[V($(Ut),{class:"layout-header",bordered:!1},{default:K(()=>[O("div",$r,[V($(he),{text:"",size:"medium",class:"collapse-btn",onClick:P},{icon:K(()=>[V($(se),{size:"18"},{default:K(()=>[r.value?(j(),Z($(Ir),{key:0})):(j(),Z($(wr),{key:1}))]),_:1})]),_:1}),k.value.length>1?(j(),Y("div",Nr,[V($(Lt),null,{default:K(()=>[(j(!0),Y(lo,null,Go(k.value,(E,D)=>(j(),Z($($t),{key:E.key,class:qo({clickable:E.clickable}),onClick:X=>E.clickable&&w(E.key)},{default:K(()=>[E.icon?(j(),Z($(se),{key:0,class:"breadcrumb-icon"},{default:K(()=>[(j(),Z(Xo(E.icon)))]),_:2},1024)):Fe("",!0),O("span",null,ye(E.label),1)]),_:2},1032,["class","onClick"]))),128))]),_:1})])):Fe("",!0)]),O("div",Br,[V($(at),{size:8},{default:K(()=>[V($(he),{text:"",size:"medium",class:"header-btn",onClick:x},{icon:K(()=>[V($(Rt),{value:u.value,max:99,"show-zero":!1},{default:K(()=>[V($(se),{size:"18"},{default:K(()=>[V($(sr))]),_:1})]),_:1},8,["value"])]),_:1}),V($(he),{text:"",size:"medium",class:"header-btn",onClick:B},{icon:K(()=>[V($(se),{size:"18"},{default:K(()=>[s.value?(j(),Z($(fr),{key:0})):(j(),Z($(gr),{key:1}))]),_:1})]),_:1}),V($(he),{text:"",size:"medium",class:"header-btn",title:"退出登录",onClick:_},{icon:K(()=>[V($(se),{size:"18"},{default:K(()=>[V($(Xe))]),_:1})]),_:1})]),_:1}),f[4]||(f[4]=O("div",{class:"divider"},null,-1)),V($(io),{options:v,trigger:"click",placement:"bottom-end",onSelect:R},{default:K(()=>{var E,D,X;return[O("div",Mr,[V($(yt),{size:"small",class:"user-avatar"},{icon:K(()=>[V($(je))]),_:1}),xe(O("div",Er,[O("div",Fr,ye(((E=$(n).adminInfo)==null?void 0:E.name)||((D=$(n).adminInfo)==null?void 0:D.username)||"管理员"),1),O("div",jr,ye((X=$(n).adminInfo)!=null&&X.is_super?"超级管理员":"管理员"),1)],512),[[Ce,!r.value]])])]}),_:1})])]),_:1}),V($(Vt),{class:"layout-content"},{default:K(()=>[O("div",Vr,[V(S)])]),_:1})]),_:1})]),_:1})}}},ln=Zo(Kr,[["__scopeId","data-v-1b64660e"]]);export{ln as default};
