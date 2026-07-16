import{p as B,E as pe,a5 as t,y as ve,A as y,C as P,aa as M,s as w,d as K,K as A,m as S,aU as be,L as q,O as E,_ as J,P as Ce,r as fe,a9 as me,U as p,aY as xe,W as D,G as ke,a0 as ye,t as Se,a2 as ze,b3 as Ie,c1 as Pe,c2 as Be,b5 as V}from"./index-CRYXIsvh.js";let H=[];const Y=new WeakMap;function $e(){H.forEach(e=>e(...Y.get(e))),H=[]}function Ue(e,...n){Y.set(e,n),!H.includes(e)&&H.push(e)===1&&requestAnimationFrame($e)}function Ae(e,n){return B(()=>{for(const l of n)if(e[l]!==void 0)return e[l];return e[n[n.length-1]]})}function Re(e,n="default",l=[]){const a=e.$slots[n];return a===void 0?l:a()}const Me={closeIconSizeTiny:"12px",closeIconSizeSmall:"12px",closeIconSizeMedium:"14px",closeIconSizeLarge:"14px",closeSizeTiny:"16px",closeSizeSmall:"16px",closeSizeMedium:"18px",closeSizeLarge:"18px",padding:"0 7px",closeMargin:"0 0 0 4px"};function we(e){const{textColor2:n,primaryColorHover:l,primaryColorPressed:u,primaryColor:a,infoColor:h,successColor:i,warningColor:o,errorColor:s,baseColor:b,borderColor:C,opacityDisabled:g,tagColor:$,closeIconColor:I,closeIconColorHover:v,closeIconColorPressed:r,borderRadiusSmall:c,fontSizeMini:f,fontSizeTiny:d,fontSizeSmall:x,fontSizeMedium:k,heightMini:z,heightTiny:m,heightSmall:T,heightMedium:O,closeColorHover:_,closeColorPressed:j,buttonColor2Hover:W,buttonColor2Pressed:F,fontWeightStrong:L}=e;return Object.assign(Object.assign({},Me),{closeBorderRadius:c,heightTiny:z,heightSmall:m,heightMedium:T,heightLarge:O,borderRadius:c,opacityDisabled:g,fontSizeTiny:f,fontSizeSmall:d,fontSizeMedium:x,fontSizeLarge:k,fontWeightStrong:L,textColorCheckable:n,textColorHoverCheckable:n,textColorPressedCheckable:n,textColorChecked:b,colorCheckable:"#0000",colorHoverCheckable:W,colorPressedCheckable:F,colorChecked:a,colorCheckedHover:l,colorCheckedPressed:u,border:`1px solid ${C}`,textColor:n,color:$,colorBordered:"rgb(250, 250, 252)",closeIconColor:I,closeIconColorHover:v,closeIconColorPressed:r,closeColorHover:_,closeColorPressed:j,borderPrimary:`1px solid ${t(a,{alpha:.3})}`,textColorPrimary:a,colorPrimary:t(a,{alpha:.12}),colorBorderedPrimary:t(a,{alpha:.1}),closeIconColorPrimary:a,closeIconColorHoverPrimary:a,closeIconColorPressedPrimary:a,closeColorHoverPrimary:t(a,{alpha:.12}),closeColorPressedPrimary:t(a,{alpha:.18}),borderInfo:`1px solid ${t(h,{alpha:.3})}`,textColorInfo:h,colorInfo:t(h,{alpha:.12}),colorBorderedInfo:t(h,{alpha:.1}),closeIconColorInfo:h,closeIconColorHoverInfo:h,closeIconColorPressedInfo:h,closeColorHoverInfo:t(h,{alpha:.12}),closeColorPressedInfo:t(h,{alpha:.18}),borderSuccess:`1px solid ${t(i,{alpha:.3})}`,textColorSuccess:i,colorSuccess:t(i,{alpha:.12}),colorBorderedSuccess:t(i,{alpha:.1}),closeIconColorSuccess:i,closeIconColorHoverSuccess:i,closeIconColorPressedSuccess:i,closeColorHoverSuccess:t(i,{alpha:.12}),closeColorPressedSuccess:t(i,{alpha:.18}),borderWarning:`1px solid ${t(o,{alpha:.35})}`,textColorWarning:o,colorWarning:t(o,{alpha:.15}),colorBorderedWarning:t(o,{alpha:.12}),closeIconColorWarning:o,closeIconColorHoverWarning:o,closeIconColorPressedWarning:o,closeColorHoverWarning:t(o,{alpha:.12}),closeColorPressedWarning:t(o,{alpha:.18}),borderError:`1px solid ${t(s,{alpha:.23})}`,textColorError:s,colorError:t(s,{alpha:.1}),colorBorderedError:t(s,{alpha:.08}),closeIconColorError:s,closeIconColorHoverError:s,closeIconColorPressedError:s,closeColorHoverError:t(s,{alpha:.12}),closeColorPressedError:t(s,{alpha:.18})})}const He={common:pe,self:we},Ee={color:Object,type:{type:String,default:"default"},round:Boolean,size:String,closable:Boolean,disabled:{type:Boolean,default:void 0}},Te=ve("tag",`
 --n-close-margin: var(--n-close-margin-top) var(--n-close-margin-right) var(--n-close-margin-bottom) var(--n-close-margin-left);
 white-space: nowrap;
 position: relative;
 box-sizing: border-box;
 cursor: default;
 display: inline-flex;
 align-items: center;
 flex-wrap: nowrap;
 padding: var(--n-padding);
 border-radius: var(--n-border-radius);
 color: var(--n-text-color);
 background-color: var(--n-color);
 transition: 
 border-color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier),
 opacity .3s var(--n-bezier);
 line-height: 1;
 height: var(--n-height);
 font-size: var(--n-font-size);
`,[y("strong",`
 font-weight: var(--n-font-weight-strong);
 `),P("border",`
 pointer-events: none;
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 border-radius: inherit;
 border: var(--n-border);
 transition: border-color .3s var(--n-bezier);
 `),P("icon",`
 display: flex;
 margin: 0 4px 0 0;
 color: var(--n-text-color);
 transition: color .3s var(--n-bezier);
 font-size: var(--n-avatar-size-override);
 `),P("avatar",`
 display: flex;
 margin: 0 6px 0 0;
 `),P("close",`
 margin: var(--n-close-margin);
 transition:
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
 `),y("round",`
 padding: 0 calc(var(--n-height) / 3);
 border-radius: calc(var(--n-height) / 2);
 `,[P("icon",`
 margin: 0 4px 0 calc((var(--n-height) - 8px) / -2);
 `),P("avatar",`
 margin: 0 6px 0 calc((var(--n-height) - 8px) / -2);
 `),y("closable",`
 padding: 0 calc(var(--n-height) / 4) 0 calc(var(--n-height) / 3);
 `)]),y("icon, avatar",[y("round",`
 padding: 0 calc(var(--n-height) / 3) 0 calc(var(--n-height) / 2);
 `)]),y("disabled",`
 cursor: not-allowed !important;
 opacity: var(--n-opacity-disabled);
 `),y("checkable",`
 cursor: pointer;
 box-shadow: none;
 color: var(--n-text-color-checkable);
 background-color: var(--n-color-checkable);
 `,[M("disabled",[w("&:hover","background-color: var(--n-color-hover-checkable);",[M("checked","color: var(--n-text-color-hover-checkable);")]),w("&:active","background-color: var(--n-color-pressed-checkable);",[M("checked","color: var(--n-text-color-pressed-checkable);")])]),y("checked",`
 color: var(--n-text-color-checked);
 background-color: var(--n-color-checked);
 `,[M("disabled",[w("&:hover","background-color: var(--n-color-checked-hover);"),w("&:active","background-color: var(--n-color-checked-pressed);")])])])]),Oe=Object.assign(Object.assign(Object.assign({},E.props),Ee),{bordered:{type:Boolean,default:void 0},checked:Boolean,checkable:Boolean,strong:Boolean,triggerClickOnClose:Boolean,onClose:[Array,Function],onMouseenter:Function,onMouseleave:Function,"onUpdate:checked":Function,onUpdateChecked:Function,internalCloseFocusable:{type:Boolean,default:!0},internalCloseIsButtonTag:{type:Boolean,default:!0},onCheckedChange:Function}),_e=ke("n-tag"),De=K({name:"Tag",props:Oe,slots:Object,setup(e){const n=fe(null),{mergedBorderedRef:l,mergedClsPrefixRef:u,inlineThemeDisabled:a,mergedRtlRef:h,mergedComponentPropsRef:i}=q(e),o=B(()=>{var r,c;return e.size||((c=(r=i==null?void 0:i.value)===null||r===void 0?void 0:r.Tag)===null||c===void 0?void 0:c.size)||"medium"}),s=E("Tag","-tag",Te,He,e,u);ye(_e,{roundRef:Se(e,"round")});function b(){if(!e.disabled&&e.checkable){const{checked:r,onCheckedChange:c,onUpdateChecked:f,"onUpdate:checked":d}=e;f&&f(!r),d&&d(!r),c&&c(!r)}}function C(r){if(e.triggerClickOnClose||r.stopPropagation(),!e.disabled){const{onClose:c}=e;c&&me(c,r)}}const g={setTextContent(r){const{value:c}=n;c&&(c.textContent=r)}},$=J("Tag",h,u),I=B(()=>{const{type:r,color:{color:c,textColor:f}={}}=e,d=o.value,{common:{cubicBezierEaseInOut:x},self:{padding:k,closeMargin:z,borderRadius:m,opacityDisabled:T,textColorCheckable:O,textColorHoverCheckable:_,textColorPressedCheckable:j,textColorChecked:W,colorCheckable:F,colorHoverCheckable:L,colorPressedCheckable:Q,colorChecked:X,colorCheckedHover:Z,colorCheckedPressed:ee,closeBorderRadius:oe,fontWeightStrong:re,[p("colorBordered",r)]:le,[p("closeSize",d)]:ae,[p("closeIconSize",d)]:ne,[p("fontSize",d)]:te,[p("height",d)]:N,[p("color",r)]:ce,[p("textColor",r)]:se,[p("border",r)]:ie,[p("closeIconColor",r)]:U,[p("closeIconColorHover",r)]:de,[p("closeIconColorPressed",r)]:he,[p("closeColorHover",r)]:ge,[p("closeColorPressed",r)]:ue}}=s.value,R=xe(z);return{"--n-font-weight-strong":re,"--n-avatar-size-override":`calc(${N} - 8px)`,"--n-bezier":x,"--n-border-radius":m,"--n-border":ie,"--n-close-icon-size":ne,"--n-close-color-pressed":ue,"--n-close-color-hover":ge,"--n-close-border-radius":oe,"--n-close-icon-color":U,"--n-close-icon-color-hover":de,"--n-close-icon-color-pressed":he,"--n-close-icon-color-disabled":U,"--n-close-margin-top":R.top,"--n-close-margin-right":R.right,"--n-close-margin-bottom":R.bottom,"--n-close-margin-left":R.left,"--n-close-size":ae,"--n-color":c||(l.value?le:ce),"--n-color-checkable":F,"--n-color-checked":X,"--n-color-checked-hover":Z,"--n-color-checked-pressed":ee,"--n-color-hover-checkable":L,"--n-color-pressed-checkable":Q,"--n-font-size":te,"--n-height":N,"--n-opacity-disabled":T,"--n-padding":k,"--n-text-color":f||se,"--n-text-color-checkable":O,"--n-text-color-checked":W,"--n-text-color-hover-checkable":_,"--n-text-color-pressed-checkable":j}}),v=a?Ce("tag",B(()=>{let r="";const{type:c,color:{color:f,textColor:d}={}}=e;return r+=c[0],r+=o.value[0],f&&(r+=`a${D(f)}`),d&&(r+=`b${D(d)}`),l.value&&(r+="c"),r}),I,e):void 0;return Object.assign(Object.assign({},g),{rtlEnabled:$,mergedClsPrefix:u,contentRef:n,mergedBordered:l,handleClick:b,handleCloseClick:C,cssVars:a?void 0:I,themeClass:v==null?void 0:v.themeClass,onRender:v==null?void 0:v.onRender})},render(){var e,n;const{mergedClsPrefix:l,rtlEnabled:u,closable:a,color:{borderColor:h}={},round:i,onRender:o,$slots:s}=this;o==null||o();const b=A(s.avatar,g=>g&&S("div",{class:`${l}-tag__avatar`},g)),C=A(s.icon,g=>g&&S("div",{class:`${l}-tag__icon`},g));return S("div",{class:[`${l}-tag`,this.themeClass,{[`${l}-tag--rtl`]:u,[`${l}-tag--strong`]:this.strong,[`${l}-tag--disabled`]:this.disabled,[`${l}-tag--checkable`]:this.checkable,[`${l}-tag--checked`]:this.checkable&&this.checked,[`${l}-tag--round`]:i,[`${l}-tag--avatar`]:b,[`${l}-tag--icon`]:C,[`${l}-tag--closable`]:a}],style:this.cssVars,onClick:this.handleClick,onMouseenter:this.onMouseenter,onMouseleave:this.onMouseleave},C||b,S("span",{class:`${l}-tag__content`,ref:"contentRef"},(n=(e=this.$slots).default)===null||n===void 0?void 0:n.call(e)),!this.checkable&&a?S(be,{clsPrefix:l,class:`${l}-tag__close`,disabled:this.disabled,onClick:this.handleCloseClick,focusable:this.internalCloseFocusable,round:i,isButtonTag:this.internalCloseIsButtonTag,absolute:!0}):null,!this.checkable&&this.mergedBordered?S("div",{class:`${l}-tag__border`,style:{borderColor:h}}):null)}}),je={gapSmall:"4px 8px",gapMedium:"8px 12px",gapLarge:"12px 16px"};function We(){return je}const Fe={self:We};let G;function Le(){if(!ze)return!0;if(G===void 0){const e=document.createElement("div");e.style.display="flex",e.style.flexDirection="column",e.style.rowGap="1px",e.appendChild(document.createElement("div")),e.appendChild(document.createElement("div")),document.body.appendChild(e);const n=e.scrollHeight===1;return document.body.removeChild(e),G=n}return G}const Ge=Object.assign(Object.assign({},E.props),{align:String,justify:{type:String,default:"start"},inline:Boolean,vertical:Boolean,reverse:Boolean,size:[String,Number,Array],wrapItem:{type:Boolean,default:!0},itemClass:String,itemStyle:[String,Object],wrap:{type:Boolean,default:!0},internalUseGap:{type:Boolean,default:void 0}}),Ve=K({name:"Space",props:Ge,setup(e){const{mergedClsPrefixRef:n,mergedRtlRef:l,mergedComponentPropsRef:u}=q(e),a=B(()=>{var o,s;return e.size||((s=(o=u==null?void 0:u.value)===null||o===void 0?void 0:o.Space)===null||s===void 0?void 0:s.size)||"medium"}),h=E("Space","-space",void 0,Fe,e,n),i=J("Space",l,n);return{useGap:Le(),rtlEnabled:i,mergedClsPrefix:n,margin:B(()=>{const o=a.value;if(Array.isArray(o))return{horizontal:o[0],vertical:o[1]};if(typeof o=="number")return{horizontal:o,vertical:o};const{self:{[p("gap",o)]:s}}=h.value,{row:b,col:C}=Be(s);return{horizontal:V(C),vertical:V(b)}})}},render(){const{vertical:e,reverse:n,align:l,inline:u,justify:a,itemClass:h,itemStyle:i,margin:o,wrap:s,mergedClsPrefix:b,rtlEnabled:C,useGap:g,wrapItem:$,internalUseGap:I}=this,v=Ie(Re(this),!1);if(!v.length)return null;const r=`${o.horizontal}px`,c=`${o.horizontal/2}px`,f=`${o.vertical}px`,d=`${o.vertical/2}px`,x=v.length-1,k=a.startsWith("space-");return S("div",{role:"none",class:[`${b}-space`,C&&`${b}-space--rtl`],style:{display:u?"inline-flex":"flex",flexDirection:e&&!n?"column":e&&n?"column-reverse":!e&&n?"row-reverse":"row",justifyContent:["start","end"].includes(a)?`flex-${a}`:a,flexWrap:!s||e?"nowrap":"wrap",marginTop:g||e?"":`-${d}`,marginBottom:g||e?"":`-${d}`,alignItems:l,gap:g?`${o.vertical}px ${o.horizontal}px`:""}},!$&&(g||I)?v:v.map((z,m)=>z.type===Pe?z:S("div",{role:"none",class:h,style:[i,{maxWidth:"100%"},g?"":e?{marginBottom:m!==x?f:""}:C?{marginLeft:k?a==="space-between"&&m===x?"":c:m!==x?r:"",marginRight:k?a==="space-between"&&m===0?"":c:"",paddingTop:d,paddingBottom:d}:{marginRight:k?a==="space-between"&&m===x?"":c:m!==x?r:"",marginLeft:k?a==="space-between"&&m===0?"":c:"",paddingTop:d,paddingBottom:d}]},z)))}});export{Ve as N,De as a,Ue as b,Re as g,_e as t,Ae as u};
