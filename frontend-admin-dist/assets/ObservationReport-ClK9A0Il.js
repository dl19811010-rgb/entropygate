import{E as pe,F as I,a5 as re,y as R,C as $,A as j,ab as Ie,s as k,d as X,m as b,ai as Be,aU as He,J as Me,a8 as Ne,aV as Ee,aM as We,aW as je,aX as Le,K as fe,N as Oe,L as be,O as Z,_ as xe,P as me,p as M,r as ge,aY as De,U as V,H as $e,I as Re,G as Fe,a0 as Ve,t as Ae,M as qe,ay as Ue,aa as Ke,aq as Se,Q as Ge,c as D,e as o,w as l,g as e,ak as we,o as h,a as oe,as as a,B as ke,aj as B,af as G,ar as Y,am as le,ap as c,l as se}from"./index-CRYXIsvh.js";import{_ as Qe}from"./_plugin-vue_export-helper-DlAUqK2U.js";import{u as Ye,N as ne,a as ie}from"./Space-DOsY5xaG.js";import{N as Je,a as he}from"./Select-DtSLODmb.js";import{u as Xe}from"./use-message-BppchCHs.js";import{N as Ze}from"./Spin-DpKgMide.js";import{N as Pe,a as ae}from"./Grid-DIUV-cue.js";import{N as Ce}from"./Divider-3l9mO-BJ.js";import{N as _e}from"./Progress-DxuYgOec.js";import"./Popover-CB8JeE3n.js";import"./format-length-B-p6aW7q.js";import"./Suffix-r3DeWvWw.js";const eo={iconMargin:"11px 8px 0 12px",iconMarginRtl:"11px 12px 0 8px",iconSize:"24px",closeIconSize:"16px",closeSize:"20px",closeMargin:"13px 14px 0 0",closeMarginRtl:"13px 0 0 14px",padding:"13px"};function oo(s){const{lineHeight:n,borderRadius:i,fontWeightStrong:d,baseColor:v,dividerColor:f,actionColor:g,textColor1:m,textColor2:x,closeColorHover:z,closeColorPressed:w,closeIconColor:P,closeIconColorHover:T,closeIconColorPressed:S,infoColor:p,successColor:H,warningColor:L,errorColor:W,fontSize:A}=s;return Object.assign(Object.assign({},eo),{fontSize:A,lineHeight:n,titleFontWeight:d,borderRadius:i,border:`1px solid ${f}`,color:g,titleTextColor:m,iconColor:x,contentTextColor:x,closeBorderRadius:i,closeColorHover:z,closeColorPressed:w,closeIconColor:P,closeIconColorHover:T,closeIconColorPressed:S,borderInfo:`1px solid ${I(v,re(p,{alpha:.25}))}`,colorInfo:I(v,re(p,{alpha:.08})),titleTextColorInfo:m,iconColorInfo:p,contentTextColorInfo:x,closeColorHoverInfo:z,closeColorPressedInfo:w,closeIconColorInfo:P,closeIconColorHoverInfo:T,closeIconColorPressedInfo:S,borderSuccess:`1px solid ${I(v,re(H,{alpha:.25}))}`,colorSuccess:I(v,re(H,{alpha:.08})),titleTextColorSuccess:m,iconColorSuccess:H,contentTextColorSuccess:x,closeColorHoverSuccess:z,closeColorPressedSuccess:w,closeIconColorSuccess:P,closeIconColorHoverSuccess:T,closeIconColorPressedSuccess:S,borderWarning:`1px solid ${I(v,re(L,{alpha:.33}))}`,colorWarning:I(v,re(L,{alpha:.08})),titleTextColorWarning:m,iconColorWarning:L,contentTextColorWarning:x,closeColorHoverWarning:z,closeColorPressedWarning:w,closeIconColorWarning:P,closeIconColorHoverWarning:T,closeIconColorPressedWarning:S,borderError:`1px solid ${I(v,re(W,{alpha:.25}))}`,colorError:I(v,re(W,{alpha:.08})),titleTextColorError:m,iconColorError:W,contentTextColorError:x,closeColorHoverError:z,closeColorPressedError:w,closeIconColorError:P,closeIconColorHoverError:T,closeIconColorPressedError:S})}const lo={common:pe,self:oo},to=R("alert",`
 line-height: var(--n-line-height);
 border-radius: var(--n-border-radius);
 position: relative;
 transition: background-color .3s var(--n-bezier);
 background-color: var(--n-color);
 text-align: start;
 word-break: break-word;
`,[$("border",`
 border-radius: inherit;
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 transition: border-color .3s var(--n-bezier);
 border: var(--n-border);
 pointer-events: none;
 `),j("closable",[R("alert-body",[$("title",`
 padding-right: 24px;
 `)])]),$("icon",{color:"var(--n-icon-color)"}),R("alert-body",{padding:"var(--n-padding)"},[$("title",{color:"var(--n-title-text-color)"}),$("content",{color:"var(--n-content-text-color)"})]),Ie({originalTransition:"transform .3s var(--n-bezier)",enterToProps:{transform:"scale(1)"},leaveToProps:{transform:"scale(0.9)"}}),$("icon",`
 position: absolute;
 left: 0;
 top: 0;
 align-items: center;
 justify-content: center;
 display: flex;
 width: var(--n-icon-size);
 height: var(--n-icon-size);
 font-size: var(--n-icon-size);
 margin: var(--n-icon-margin);
 `),$("close",`
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 position: absolute;
 right: 0;
 top: 0;
 margin: var(--n-close-margin);
 `),j("show-icon",[R("alert-body",{paddingLeft:"calc(var(--n-icon-margin-left) + var(--n-icon-size) + var(--n-icon-margin-right))"})]),j("right-adjust",[R("alert-body",{paddingRight:"calc(var(--n-close-size) + var(--n-padding) + 2px)"})]),R("alert-body",`
 border-radius: var(--n-border-radius);
 transition: border-color .3s var(--n-bezier);
 `,[$("title",`
 transition: color .3s var(--n-bezier);
 font-size: 16px;
 line-height: 19px;
 font-weight: var(--n-title-font-weight);
 `,[k("& +",[$("content",{marginTop:"9px"})])]),$("content",{transition:"color .3s var(--n-bezier)",fontSize:"var(--n-font-size)"})]),$("icon",{transition:"color .3s var(--n-bezier)"})]),ro=Object.assign(Object.assign({},Z.props),{title:String,showIcon:{type:Boolean,default:!0},type:{type:String,default:"default"},bordered:{type:Boolean,default:!0},closable:Boolean,onClose:Function,onAfterLeave:Function,onAfterHide:Function}),de=X({name:"Alert",inheritAttrs:!1,props:ro,slots:Object,setup(s){const{mergedClsPrefixRef:n,mergedBorderedRef:i,inlineThemeDisabled:d,mergedRtlRef:v}=be(s),f=Z("Alert","-alert",to,lo,s,n),g=xe("Alert",v,n),m=M(()=>{const{common:{cubicBezierEaseInOut:S},self:p}=f.value,{fontSize:H,borderRadius:L,titleFontWeight:W,lineHeight:A,iconSize:N,iconMargin:q,iconMarginRtl:E,closeIconSize:ve,closeBorderRadius:O,closeSize:ee,closeMargin:Q,closeMarginRtl:u,padding:t}=p,{type:y}=s,{left:te,right:r}=De(q);return{"--n-bezier":S,"--n-color":p[V("color",y)],"--n-close-icon-size":ve,"--n-close-border-radius":O,"--n-close-color-hover":p[V("closeColorHover",y)],"--n-close-color-pressed":p[V("closeColorPressed",y)],"--n-close-icon-color":p[V("closeIconColor",y)],"--n-close-icon-color-hover":p[V("closeIconColorHover",y)],"--n-close-icon-color-pressed":p[V("closeIconColorPressed",y)],"--n-icon-color":p[V("iconColor",y)],"--n-border":p[V("border",y)],"--n-title-text-color":p[V("titleTextColor",y)],"--n-content-text-color":p[V("contentTextColor",y)],"--n-line-height":A,"--n-border-radius":L,"--n-font-size":H,"--n-title-font-weight":W,"--n-icon-size":N,"--n-icon-margin":q,"--n-icon-margin-rtl":E,"--n-close-size":ee,"--n-close-margin":Q,"--n-close-margin-rtl":u,"--n-padding":t,"--n-icon-margin-left":te,"--n-icon-margin-right":r}}),x=d?me("alert",M(()=>s.type[0]),m,s):void 0,z=ge(!0),w=()=>{const{onAfterLeave:S,onAfterHide:p}=s;S&&S(),p&&p()};return{rtlEnabled:g,mergedClsPrefix:n,mergedBordered:i,visible:z,handleCloseClick:()=>{var S;Promise.resolve((S=s.onClose)===null||S===void 0?void 0:S.call(s)).then(p=>{p!==!1&&(z.value=!1)})},handleAfterLeave:()=>{w()},mergedTheme:f,cssVars:d?void 0:m,themeClass:x==null?void 0:x.themeClass,onRender:x==null?void 0:x.onRender}},render(){var s;return(s=this.onRender)===null||s===void 0||s.call(this),b(Oe,{onAfterLeave:this.handleAfterLeave},{default:()=>{const{mergedClsPrefix:n,$slots:i}=this,d={class:[`${n}-alert`,this.themeClass,this.closable&&`${n}-alert--closable`,this.showIcon&&`${n}-alert--show-icon`,!this.title&&this.closable&&`${n}-alert--right-adjust`,this.rtlEnabled&&`${n}-alert--rtl`],style:this.cssVars,role:"alert"};return this.visible?b("div",Object.assign({},Be(this.$attrs,d)),this.closable&&b(He,{clsPrefix:n,class:`${n}-alert__close`,onClick:this.handleCloseClick}),this.bordered&&b("div",{class:`${n}-alert__border`}),this.showIcon&&b("div",{class:`${n}-alert__icon`,"aria-hidden":"true"},Me(i.icon,()=>[b(Ne,{clsPrefix:n},{default:()=>{switch(this.type){case"success":return b(Le,null);case"info":return b(je,null);case"warning":return b(We,null);case"error":return b(Ee,null);default:return null}}})])),b("div",{class:[`${n}-alert-body`,this.mergedBordered&&`${n}-alert-body--bordered`]},fe(i.header,v=>{const f=v||this.title;return f?b("div",{class:`${n}-alert-body__title`},f):null}),i.default&&b("div",{class:`${n}-alert-body__content`},i))):null}})}});function no(s){const{textColor2:n,cardColor:i,modalColor:d,popoverColor:v,dividerColor:f,borderRadius:g,fontSize:m,hoverColor:x}=s;return{textColor:n,color:i,colorHover:x,colorModal:d,colorHoverModal:I(d,x),colorPopover:v,colorHoverPopover:I(v,x),borderColor:f,borderColorModal:I(d,f),borderColorPopover:I(v,f),borderRadius:g,fontSize:m}}const ao={common:pe,self:no};function so(s){const{textColor2:n,textColor3:i,fontSize:d,fontWeight:v}=s;return{labelFontSize:d,labelFontWeight:v,valueFontWeight:v,valueFontSize:"24px",labelTextColor:i,valuePrefixTextColor:n,valueSuffixTextColor:n,valueTextColor:n}}const io={common:pe,self:so},uo={thPaddingSmall:"6px",thPaddingMedium:"12px",thPaddingLarge:"12px",tdPaddingSmall:"6px",tdPaddingMedium:"12px",tdPaddingLarge:"12px"};function co(s){const{dividerColor:n,cardColor:i,modalColor:d,popoverColor:v,tableHeaderColor:f,tableColorStriped:g,textColor1:m,textColor2:x,borderRadius:z,fontWeightStrong:w,lineHeight:P,fontSizeSmall:T,fontSizeMedium:S,fontSizeLarge:p}=s;return Object.assign(Object.assign({},uo),{fontSizeSmall:T,fontSizeMedium:S,fontSizeLarge:p,lineHeight:P,borderRadius:z,borderColor:I(i,n),borderColorModal:I(d,n),borderColorPopover:I(v,n),tdColor:i,tdColorModal:d,tdColorPopover:v,tdColorStriped:I(i,g),tdColorStripedModal:I(d,g),tdColorStripedPopover:I(v,g),thColor:I(i,f),thColorModal:I(d,f),thColorPopover:I(v,f),thTextColor:m,tdTextColor:x,thFontWeight:w})}const vo={common:pe,self:co},fo={headerFontSize1:"30px",headerFontSize2:"22px",headerFontSize3:"18px",headerFontSize4:"16px",headerFontSize5:"16px",headerFontSize6:"16px",headerMargin1:"28px 0 20px 0",headerMargin2:"28px 0 20px 0",headerMargin3:"28px 0 20px 0",headerMargin4:"28px 0 18px 0",headerMargin5:"28px 0 18px 0",headerMargin6:"28px 0 18px 0",headerPrefixWidth1:"16px",headerPrefixWidth2:"16px",headerPrefixWidth3:"12px",headerPrefixWidth4:"12px",headerPrefixWidth5:"12px",headerPrefixWidth6:"12px",headerBarWidth1:"4px",headerBarWidth2:"4px",headerBarWidth3:"3px",headerBarWidth4:"3px",headerBarWidth5:"3px",headerBarWidth6:"3px",pMargin:"16px 0 16px 0",liMargin:".25em 0 0 0",olPadding:"0 0 0 2em",ulPadding:"0 0 0 2em"};function go(s){const{primaryColor:n,textColor2:i,borderColor:d,lineHeight:v,fontSize:f,borderRadiusSmall:g,dividerColor:m,fontWeightStrong:x,textColor1:z,textColor3:w,infoColor:P,warningColor:T,errorColor:S,successColor:p,codeColor:H}=s;return Object.assign(Object.assign({},fo),{aTextColor:n,blockquoteTextColor:i,blockquotePrefixColor:d,blockquoteLineHeight:v,blockquoteFontSize:f,codeBorderRadius:g,liTextColor:i,liLineHeight:v,liFontSize:f,hrColor:m,headerFontWeight:x,headerTextColor:z,pTextColor:i,pTextColor1Depth:z,pTextColor2Depth:i,pTextColor3Depth:w,pLineHeight:v,pFontSize:f,headerBarColor:n,headerBarColorPrimary:n,headerBarColorInfo:P,headerBarColorError:S,headerBarColorWarning:T,headerBarColorSuccess:p,textColor:i,textColor1Depth:z,textColor2Depth:i,textColor3Depth:w,textColorPrimary:n,textColorInfo:P,textColorSuccess:p,textColorWarning:T,textColorError:S,codeTextColor:i,codeColor:H,codeBorder:"1px solid #0000"})}const po={common:pe,self:go},bo=k([R("list",`
 --n-merged-border-color: var(--n-border-color);
 --n-merged-color: var(--n-color);
 --n-merged-color-hover: var(--n-color-hover);
 margin: 0;
 font-size: var(--n-font-size);
 transition:
 background-color .3s var(--n-bezier),
 color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 padding: 0;
 list-style-type: none;
 color: var(--n-text-color);
 background-color: var(--n-merged-color);
 `,[j("show-divider",[R("list-item",[k("&:not(:last-child)",[$("divider",`
 background-color: var(--n-merged-border-color);
 `)])])]),j("clickable",[R("list-item",`
 cursor: pointer;
 `)]),j("bordered",`
 border: 1px solid var(--n-merged-border-color);
 border-radius: var(--n-border-radius);
 `),j("hoverable",[R("list-item",`
 border-radius: var(--n-border-radius);
 `,[k("&:hover",`
 background-color: var(--n-merged-color-hover);
 `,[$("divider",`
 background-color: transparent;
 `)])])]),j("bordered, hoverable",[R("list-item",`
 padding: 12px 20px;
 `),$("header, footer",`
 padding: 12px 20px;
 `)]),$("header, footer",`
 padding: 12px 0;
 box-sizing: border-box;
 transition: border-color .3s var(--n-bezier);
 `,[k("&:not(:last-child)",`
 border-bottom: 1px solid var(--n-merged-border-color);
 `)]),R("list-item",`
 position: relative;
 padding: 12px 0; 
 box-sizing: border-box;
 display: flex;
 flex-wrap: nowrap;
 align-items: center;
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `,[$("prefix",`
 margin-right: 20px;
 flex: 0;
 `),$("suffix",`
 margin-left: 20px;
 flex: 0;
 `),$("main",`
 flex: 1;
 `),$("divider",`
 height: 1px;
 position: absolute;
 bottom: 0;
 left: 0;
 right: 0;
 background-color: transparent;
 transition: background-color .3s var(--n-bezier);
 pointer-events: none;
 `)])]),$e(R("list",`
 --n-merged-color-hover: var(--n-color-hover-modal);
 --n-merged-color: var(--n-color-modal);
 --n-merged-border-color: var(--n-border-color-modal);
 `)),Re(R("list",`
 --n-merged-color-hover: var(--n-color-hover-popover);
 --n-merged-color: var(--n-color-popover);
 --n-merged-border-color: var(--n-border-color-popover);
 `))]),mo=Object.assign(Object.assign({},Z.props),{size:{type:String,default:"medium"},bordered:Boolean,clickable:Boolean,hoverable:Boolean,showDivider:{type:Boolean,default:!0}}),Te=Fe("n-list"),ye=X({name:"List",props:mo,slots:Object,setup(s){const{mergedClsPrefixRef:n,inlineThemeDisabled:i,mergedRtlRef:d}=be(s),v=xe("List",d,n),f=Z("List","-list",bo,ao,s,n);Ve(Te,{showDividerRef:Ae(s,"showDivider"),mergedClsPrefixRef:n});const g=M(()=>{const{common:{cubicBezierEaseInOut:x},self:{fontSize:z,textColor:w,color:P,colorModal:T,colorPopover:S,borderColor:p,borderColorModal:H,borderColorPopover:L,borderRadius:W,colorHover:A,colorHoverModal:N,colorHoverPopover:q}}=f.value;return{"--n-font-size":z,"--n-bezier":x,"--n-text-color":w,"--n-color":P,"--n-border-radius":W,"--n-border-color":p,"--n-border-color-modal":H,"--n-border-color-popover":L,"--n-color-modal":T,"--n-color-popover":S,"--n-color-hover":A,"--n-color-hover-modal":N,"--n-color-hover-popover":q}}),m=i?me("list",void 0,g,s):void 0;return{mergedClsPrefix:n,rtlEnabled:v,cssVars:i?void 0:g,themeClass:m==null?void 0:m.themeClass,onRender:m==null?void 0:m.onRender}},render(){var s;const{$slots:n,mergedClsPrefix:i,onRender:d}=this;return d==null||d(),b("ul",{class:[`${i}-list`,this.rtlEnabled&&`${i}-list--rtl`,this.bordered&&`${i}-list--bordered`,this.showDivider&&`${i}-list--show-divider`,this.hoverable&&`${i}-list--hoverable`,this.clickable&&`${i}-list--clickable`,this.themeClass],style:this.cssVars},n.header?b("div",{class:`${i}-list__header`},n.header()):null,(s=n.default)===null||s===void 0?void 0:s.call(n),n.footer?b("div",{class:`${i}-list__footer`},n.footer()):null)}}),ze=X({name:"ListItem",slots:Object,setup(){const s=qe(Te,null);return s||Ue("list-item","`n-list-item` must be placed in `n-list`."),{showDivider:s.showDividerRef,mergedClsPrefix:s.mergedClsPrefixRef}},render(){const{$slots:s,mergedClsPrefix:n}=this;return b("li",{class:`${n}-list-item`},s.prefix?b("div",{class:`${n}-list-item__prefix`},s.prefix()):null,s.default?b("div",{class:`${n}-list-item__main`},s):null,s.suffix?b("div",{class:`${n}-list-item__suffix`},s.suffix()):null,this.showDivider&&b("div",{class:`${n}-list-item__divider`}))}}),ho=R("statistic",[$("label",`
 font-weight: var(--n-label-font-weight);
 transition: .3s color var(--n-bezier);
 font-size: var(--n-label-font-size);
 color: var(--n-label-text-color);
 `),R("statistic-value",`
 margin-top: 4px;
 font-weight: var(--n-value-font-weight);
 `,[$("prefix",`
 margin: 0 4px 0 0;
 font-size: var(--n-value-font-size);
 transition: .3s color var(--n-bezier);
 color: var(--n-value-prefix-text-color);
 `,[R("icon",{verticalAlign:"-0.125em"})]),$("content",`
 font-size: var(--n-value-font-size);
 transition: .3s color var(--n-bezier);
 color: var(--n-value-text-color);
 `),$("suffix",`
 margin: 0 0 0 4px;
 font-size: var(--n-value-font-size);
 transition: .3s color var(--n-bezier);
 color: var(--n-value-suffix-text-color);
 `,[R("icon",{verticalAlign:"-0.125em"})])])]),xo=Object.assign(Object.assign({},Z.props),{tabularNums:Boolean,label:String,value:[String,Number]}),F=X({name:"Statistic",props:xo,slots:Object,setup(s){const{mergedClsPrefixRef:n,inlineThemeDisabled:i,mergedRtlRef:d}=be(s),v=Z("Statistic","-statistic",ho,io,s,n),f=xe("Statistic",d,n),g=M(()=>{const{self:{labelFontWeight:x,valueFontSize:z,valueFontWeight:w,valuePrefixTextColor:P,labelTextColor:T,valueSuffixTextColor:S,valueTextColor:p,labelFontSize:H},common:{cubicBezierEaseInOut:L}}=v.value;return{"--n-bezier":L,"--n-label-font-size":H,"--n-label-font-weight":x,"--n-label-text-color":T,"--n-value-font-weight":w,"--n-value-font-size":z,"--n-value-prefix-text-color":P,"--n-value-suffix-text-color":S,"--n-value-text-color":p}}),m=i?me("statistic",void 0,g,s):void 0;return{rtlEnabled:f,mergedClsPrefix:n,cssVars:i?void 0:g,themeClass:m==null?void 0:m.themeClass,onRender:m==null?void 0:m.onRender}},render(){var s;const{mergedClsPrefix:n,$slots:{default:i,label:d,prefix:v,suffix:f}}=this;return(s=this.onRender)===null||s===void 0||s.call(this),b("div",{class:[`${n}-statistic`,this.themeClass,this.rtlEnabled&&`${n}-statistic--rtl`],style:this.cssVars},fe(d,g=>b("div",{class:`${n}-statistic__label`},this.label||g)),b("div",{class:`${n}-statistic-value`,style:{fontVariantNumeric:this.tabularNums?"tabular-nums":""}},fe(v,g=>g&&b("span",{class:`${n}-statistic-value__prefix`},g)),this.value!==void 0?b("span",{class:`${n}-statistic-value__content`},this.value):fe(i,g=>g&&b("span",{class:`${n}-statistic-value__content`},g)),fe(f,g=>g&&b("span",{class:`${n}-statistic-value__suffix`},g))))}}),Co=k([R("table",`
 font-size: var(--n-font-size);
 font-variant-numeric: tabular-nums;
 line-height: var(--n-line-height);
 width: 100%;
 border-radius: var(--n-border-radius) var(--n-border-radius) 0 0;
 text-align: left;
 border-collapse: separate;
 border-spacing: 0;
 overflow: hidden;
 background-color: var(--n-td-color);
 border-color: var(--n-merged-border-color);
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
 --n-merged-border-color: var(--n-border-color);
 `,[k("th",`
 white-space: nowrap;
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
 text-align: inherit;
 padding: var(--n-th-padding);
 vertical-align: inherit;
 text-transform: none;
 border: 0px solid var(--n-merged-border-color);
 font-weight: var(--n-th-font-weight);
 color: var(--n-th-text-color);
 background-color: var(--n-th-color);
 border-bottom: 1px solid var(--n-merged-border-color);
 border-right: 1px solid var(--n-merged-border-color);
 `,[k("&:last-child",`
 border-right: 0px solid var(--n-merged-border-color);
 `)]),k("td",`
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier),
 color .3s var(--n-bezier);
 padding: var(--n-td-padding);
 color: var(--n-td-text-color);
 background-color: var(--n-td-color);
 border: 0px solid var(--n-merged-border-color);
 border-right: 1px solid var(--n-merged-border-color);
 border-bottom: 1px solid var(--n-merged-border-color);
 `,[k("&:last-child",`
 border-right: 0px solid var(--n-merged-border-color);
 `)]),j("bordered",`
 border: 1px solid var(--n-merged-border-color);
 border-radius: var(--n-border-radius);
 `,[k("tr",[k("&:last-child",[k("td",`
 border-bottom: 0 solid var(--n-merged-border-color);
 `)])])]),j("single-line",[k("th",`
 border-right: 0px solid var(--n-merged-border-color);
 `),k("td",`
 border-right: 0px solid var(--n-merged-border-color);
 `)]),j("single-column",[k("tr",[k("&:not(:last-child)",[k("td",`
 border-bottom: 0px solid var(--n-merged-border-color);
 `)])])]),j("striped",[k("tr:nth-of-type(even)",[k("td","background-color: var(--n-td-color-striped)")])]),Ke("bottom-bordered",[k("tr",[k("&:last-child",[k("td",`
 border-bottom: 0px solid var(--n-merged-border-color);
 `)])])])]),$e(R("table",`
 background-color: var(--n-td-color-modal);
 --n-merged-border-color: var(--n-border-color-modal);
 `,[k("th",`
 background-color: var(--n-th-color-modal);
 `),k("td",`
 background-color: var(--n-td-color-modal);
 `)])),Re(R("table",`
 background-color: var(--n-td-color-popover);
 --n-merged-border-color: var(--n-border-color-popover);
 `,[k("th",`
 background-color: var(--n-th-color-popover);
 `),k("td",`
 background-color: var(--n-td-color-popover);
 `)]))]),_o=Object.assign(Object.assign({},Z.props),{bordered:{type:Boolean,default:!0},bottomBordered:{type:Boolean,default:!0},singleLine:{type:Boolean,default:!0},striped:Boolean,singleColumn:Boolean,size:String}),ue=X({name:"Table",props:_o,setup(s){const{mergedClsPrefixRef:n,inlineThemeDisabled:i,mergedRtlRef:d,mergedComponentPropsRef:v}=be(s),f=M(()=>{var w,P;return s.size||((P=(w=v==null?void 0:v.value)===null||w===void 0?void 0:w.Table)===null||P===void 0?void 0:P.size)||"medium"}),g=Z("Table","-table",Co,vo,s,n),m=xe("Table",d,n),x=M(()=>{const w=f.value,{self:{borderColor:P,tdColor:T,tdColorModal:S,tdColorPopover:p,thColor:H,thColorModal:L,thColorPopover:W,thTextColor:A,tdTextColor:N,borderRadius:q,thFontWeight:E,lineHeight:ve,borderColorModal:O,borderColorPopover:ee,tdColorStriped:Q,tdColorStripedModal:u,tdColorStripedPopover:t,[V("fontSize",w)]:y,[V("tdPadding",w)]:te,[V("thPadding",w)]:r},common:{cubicBezierEaseInOut:U}}=g.value;return{"--n-bezier":U,"--n-td-color":T,"--n-td-color-modal":S,"--n-td-color-popover":p,"--n-td-text-color":N,"--n-border-color":P,"--n-border-color-modal":O,"--n-border-color-popover":ee,"--n-border-radius":q,"--n-font-size":y,"--n-th-color":H,"--n-th-color-modal":L,"--n-th-color-popover":W,"--n-th-font-weight":E,"--n-th-text-color":A,"--n-line-height":ve,"--n-td-padding":te,"--n-th-padding":r,"--n-td-color-striped":Q,"--n-td-color-striped-modal":u,"--n-td-color-striped-popover":t}}),z=i?me("table",M(()=>f.value[0]),x,s):void 0;return{rtlEnabled:m,mergedClsPrefix:n,cssVars:i?void 0:x,themeClass:z==null?void 0:z.themeClass,onRender:z==null?void 0:z.onRender}},render(){var s;const{mergedClsPrefix:n}=this;return(s=this.onRender)===null||s===void 0||s.call(this),b("table",{class:[`${n}-table`,this.themeClass,{[`${n}-table--rtl`]:this.rtlEnabled,[`${n}-table--bottom-bordered`]:this.bottomBordered,[`${n}-table--bordered`]:this.bordered,[`${n}-table--single-line`]:this.singleLine,[`${n}-table--single-column`]:this.singleColumn,[`${n}-table--striped`]:this.striped}],style:this.cssVars},this.$slots)}}),C=X({name:"Td",render(){return b("td",null,this.$slots)}}),_=X({name:"Th",render(){return b("th",null,this.$slots)}}),ce=X({name:"Thead",render(){return b("thead",null,this.$slots)}}),K=X({name:"Tr",render(){return b("tr",null,this.$slots)}}),yo=R("text",`
 transition: color .3s var(--n-bezier);
 color: var(--n-text-color);
`,[j("strong",`
 font-weight: var(--n-font-weight-strong);
 `),j("italic",{fontStyle:"italic"}),j("underline",{textDecoration:"underline"}),j("code",`
 line-height: 1.4;
 display: inline-block;
 font-family: var(--n-font-famliy-mono);
 transition: 
 color .3s var(--n-bezier),
 border-color .3s var(--n-bezier),
 background-color .3s var(--n-bezier);
 box-sizing: border-box;
 padding: .05em .35em 0 .35em;
 border-radius: var(--n-code-border-radius);
 font-size: .9em;
 color: var(--n-code-text-color);
 background-color: var(--n-code-color);
 border: var(--n-code-border);
 `)]),zo=Object.assign(Object.assign({},Z.props),{code:Boolean,type:{type:String,default:"default"},delete:Boolean,strong:Boolean,italic:Boolean,underline:Boolean,depth:[String,Number],tag:String,as:{type:String,validator:()=>!0,default:void 0}}),J=X({name:"Text",props:zo,setup(s){const{mergedClsPrefixRef:n,inlineThemeDisabled:i}=be(s),d=Z("Typography","-text",yo,po,s,n),v=M(()=>{const{depth:g,type:m}=s,x=m==="default"?g===void 0?"textColor":`textColor${g}Depth`:V("textColor",m),{common:{fontWeightStrong:z,fontFamilyMono:w,cubicBezierEaseInOut:P},self:{codeTextColor:T,codeBorderRadius:S,codeColor:p,codeBorder:H,[x]:L}}=d.value;return{"--n-bezier":P,"--n-text-color":L,"--n-font-weight-strong":z,"--n-font-famliy-mono":w,"--n-code-border-radius":S,"--n-code-text-color":T,"--n-code-color":p,"--n-code-border":H}}),f=i?me("text",M(()=>`${s.type[0]}${s.depth||""}`),v,s):void 0;return{mergedClsPrefix:n,compitableTag:Ye(s,["as","tag"]),cssVars:i?void 0:v,themeClass:f==null?void 0:f.themeClass,onRender:f==null?void 0:f.onRender}},render(){var s,n,i;const{mergedClsPrefix:d}=this;(s=this.onRender)===null||s===void 0||s.call(this);const v=[`${d}-text`,this.themeClass,{[`${d}-text--code`]:this.code,[`${d}-text--delete`]:this.delete,[`${d}-text--strong`]:this.strong,[`${d}-text--italic`]:this.italic,[`${d}-text--underline`]:this.underline}],f=(i=(n=this.$slots).default)===null||i===void 0?void 0:i.call(n);return this.code?b("code",{class:v,style:this.cssVars},this.delete?b("del",null,f):f):this.delete?b("del",{class:v,style:this.cssVars},f):b(this.compitableTag||"span",{class:v,style:this.cssVars},f)}});function So(s){return Se({url:"/crawler/daily-report",method:"get",params:s?{date:s}:{}})}function wo(s=30){return Se({url:"/crawler/daily-report/history",method:"get",params:{days:s}})}function ko(s){return Se({url:"/crawler/daily-report/generate",method:"post",data:s?{date:s}:{}})}const Po={key:0},$o={key:1},Ro={__name:"ObservationReport",setup(s){const n=Xe(),i=ge(!1),d=ge(null),v=ge([]),f=ge(null),g=(()=>{const u=new Date;return new Date(u.getTime()+8*3600*1e3).toISOString().slice(0,10)})(),m=M(()=>{const u=[{label:`今日 (${g})`,value:g}];for(const t of v.value)u.push({label:t.date,value:t.date});return u});async function x(){var u;try{const t=await wo(30);v.value=((u=t.data)==null?void 0:u.items)||[]}catch{v.value=[]}}async function z(u){var t;i.value=!0;try{const y=await So(u);d.value=y.data||null,f.value=((t=d.value)==null?void 0:t.date)||u}catch{d.value=null,n.warning("该日期暂无报告，可点击「生成今日报告」创建")}finally{i.value=!1}}async function w(){var u,t;i.value=!0;try{const y=await ko(f.value&&f.value!==g?f.value:null);d.value=y.data||null,f.value=(u=d.value)==null?void 0:u.date,await x(),n.success(`已生成 ${(t=d.value)==null?void 0:t.date} 的观察报告`)}catch(y){n.error("生成失败："+(y.message||"未知错误"))}finally{i.value=!1}}function P(){var te;if(!((te=d.value)!=null&&te.md_content)){n.warning("报告内容为空，无法下载");return}const u=new Blob([d.value.md_content],{type:"text/markdown;charset=utf-8"}),t=URL.createObjectURL(u),y=document.createElement("a");y.href=t,y.download=`entropygate-observation-${d.value.date}.md`,document.body.appendChild(y),y.click(),document.body.removeChild(y),URL.revokeObjectURL(t)}function T(u){return u==="healthy"?"success":u==="degraded"?"warning":"error"}function S(u){return{high:"error",medium:"warning",low:"success"}[u]||"default"}function p(u){return u>=95?"success":u>=80?"warning":"error"}function H(u){return{High:"success",Medium:"warning",Low:"error"}[u]||"default"}function L(u){return u?"success":"error"}const W=M(()=>{var u;return((u=d.value)==null?void 0:u.runtime_health)||{}}),A=M(()=>{var u;return((u=d.value)==null?void 0:u.coverage_snapshot)||{}}),N=M(()=>{var u;return((u=d.value)==null?void 0:u.data_quality)||{}}),q=M(()=>{var u;return((u=d.value)==null?void 0:u.editorial_summary)||{}}),E=M(()=>{var u;return((u=d.value)==null?void 0:u.homepage_readiness)||{}}),ve=M(()=>{var u;return((u=d.value)==null?void 0:u.recommendations)||[]}),O=M(()=>{var u,t;return((t=(u=d.value)==null?void 0:u.coverage_snapshot)==null?void 0:t.intelligence_yield)||{}}),ee=M(()=>{var u,t;return((t=(u=d.value)==null?void 0:u.coverage_snapshot)==null?void 0:t.source_performance)||{rows:[]}}),Q=M(()=>{var u,t;return((t=(u=d.value)==null?void 0:u.editorial_summary)==null?void 0:t.human_review_notes)||{}});return Ge(async()=>{await x(),await z(g)}),(u,t)=>{const y=we("NTbody"),te=we("NThing");return h(),D("div",null,[o(e(ne),{justify:"space-between",align:"center",class:"page-head"},{default:l(()=>[oe("div",null,[t[3]||(t[3]=oe("h2",{class:"page-title"},"每日观察报告",-1)),o(e(J),{depth:"3"},{default:l(()=>[...t[2]||(t[2]=[a("EntropyGate AI 的驾驶舱 · 所有迭代决策的唯一事实来源",-1)])]),_:1})]),o(e(ne),null,{default:l(()=>[o(e(Je),{value:f.value,"onUpdate:value":[t[0]||(t[0]=r=>f.value=r),t[1]||(t[1]=r=>z(r))],options:m.value,placeholder:"选择日期",style:{width:"200px"}},null,8,["value","options"]),o(e(ke),{type:"primary",loading:i.value,onClick:w},{default:l(()=>[...t[4]||(t[4]=[a("生成今日报告",-1)])]),_:1},8,["loading"]),o(e(ke),{onClick:P},{default:l(()=>[...t[5]||(t[5]=[a("下载 MD",-1)])]),_:1})]),_:1})]),_:1}),o(e(Ze),{show:i.value},{default:l(()=>[d.value?(h(),D(G,{key:1},[o(e(Y),{title:"1. Runtime Health（系统健康）",bordered:!0,class:"section"},{default:l(()=>[o(e(Pe),{cols:4,"x-gap":12,"y-gap":12},{default:l(()=>[o(e(ae),null,{default:l(()=>[o(e(F),{label:"调度器",value:W.value.scheduler_running?"运行中":"异常"},null,8,["value"])]),_:1}),o(e(ae),null,{default:l(()=>[o(e(F),{label:"总任务",value:W.value.total_tasks||0},null,8,["value"])]),_:1}),o(e(ae),null,{default:l(()=>[o(e(F),{label:"成功",value:W.value.completed_tasks||0},null,8,["value"])]),_:1}),o(e(ae),null,{default:l(()=>[o(e(F),{label:"失败/错误",value:(W.value.failed_tasks||0)+" / "+(W.value.api_errors||0)},null,8,["value"])]),_:1})]),_:1}),o(e(Ce),{"title-placement":"left"},{default:l(()=>[...t[6]||(t[6]=[a("Source Health",-1)])]),_:1}),o(e(ue),{"single-line":!1,size:"small"},{default:l(()=>[o(e(ce),null,{default:l(()=>[o(e(K),null,{default:l(()=>[o(e(_),null,{default:l(()=>[...t[7]||(t[7]=[a("Source",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[8]||(t[8]=[a("Tier",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[9]||(t[9]=[a("维度",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[10]||(t[10]=[a("状态",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[11]||(t[11]=[a("最近成功",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[12]||(t[12]=[a("今日文章",-1)])]),_:1})]),_:1})]),_:1}),o(y,null,{default:l(()=>[(h(!0),D(G,null,le(W.value.source_health,r=>(h(),B(e(K),{key:r.name},{default:l(()=>[o(e(C),null,{default:l(()=>[a(c(r.name),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.tier),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.dimension),1)]),_:2},1024),o(e(C),null,{default:l(()=>[o(e(ie),{type:T(r.health),size:"small"},{default:l(()=>[a(c(r.health),1)]),_:2},1032,["type"])]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.last_success),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.today_articles),1)]),_:2},1024)]),_:2},1024))),128))]),_:1})]),_:1})]),_:1}),o(e(Y),{title:"2. Observation Coverage（观察覆盖）",class:"section"},{default:l(()=>[o(e(J),{depth:"3"},{default:l(()=>[t[13]||(t[13]=a(" 今日共观察 ",-1)),oe("b",null,c(A.value.total_articles),1),a(" 篇 · 信号 "+c(A.value.total_signals)+" · 事件 "+c(A.value.total_events)+" · 头条候选 "+c(A.value.total_headlines),1)]),_:1}),o(e(ue),{"single-line":!1,size:"small",class:"mt"},{default:l(()=>[o(e(ce),null,{default:l(()=>[o(e(K),null,{default:l(()=>[o(e(_),null,{default:l(()=>[...t[14]||(t[14]=[a("维度",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[15]||(t[15]=[a("Articles",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[16]||(t[16]=[a("Signals",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[17]||(t[17]=[a("Events",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[18]||(t[18]=[a("Headlines",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[19]||(t[19]=[a("状态",-1)])]),_:1})]),_:1})]),_:1}),o(y,null,{default:l(()=>[(h(!0),D(G,null,le(A.value.dimensions,r=>(h(),B(e(K),{key:r.key},{default:l(()=>[o(e(C),null,{default:l(()=>[a(c(r.label),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.articles),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.signals),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.events),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.headlines),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.status),1)]),_:2},1024)]),_:2},1024))),128))]),_:1})]),_:1})]),_:1}),o(e(Y),{title:"5. Intelligence Yield（智能产出率 ⭐）",class:"section"},{default:l(()=>[o(e(ne),{align:"center",justify:"space-between"},{default:l(()=>[oe("div",null,[o(e(F),{label:"Intelligence Yield",value:(O.value.yield_rate!=null?O.value.yield_rate:0)+"%"},null,8,["value"]),o(e(J),{depth:"3",class:"block mt"},{default:l(()=>[a("Homepage Ready "+c(O.value.homepage_ready||0)+" / Collected "+c(O.value.collected||0),1)]),_:1})]),o(e(_e),{type:"dashboard",percentage:O.value.yield_rate||0,color:(O.value.yield_rate||0)>=1?"#18a058":"#f0a020",height:90},null,8,["percentage","color"])]),_:1}),O.value.funnel&&O.value.funnel.length?(h(),B(e(ue),{key:0,"single-line":!1,size:"small",class:"mt"},{default:l(()=>[o(e(ce),null,{default:l(()=>[o(e(K),null,{default:l(()=>[o(e(_),null,{default:l(()=>[...t[20]||(t[20]=[a("阶段",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[21]||(t[21]=[a("数量",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[22]||(t[22]=[a("占比",-1)])]),_:1})]),_:1})]),_:1}),o(y,null,{default:l(()=>[(h(!0),D(G,null,le(O.value.funnel,(r,U)=>(h(),B(e(K),{key:U},{default:l(()=>[o(e(C),null,{default:l(()=>[a(c(r.label)+"（"+c(r.stage)+"）",1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.count),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.ratio)+"%",1)]),_:2},1024)]),_:2},1024))),128))]),_:1})]),_:1})):se("",!0),o(e(de),{type:"default",class:"mt",title:O.value.note||"核心北极星指标：衡量采集系统是在增加价值还是制造噪音。"},null,8,["title"])]),_:1}),o(e(Y),{title:"6. Source Performance（来源表现）",class:"section"},{default:l(()=>[ee.value.rows&&ee.value.rows.length?(h(),B(e(ue),{key:0,"single-line":!1,size:"small"},{default:l(()=>[o(e(ce),null,{default:l(()=>[o(e(K),null,{default:l(()=>[o(e(_),null,{default:l(()=>[...t[23]||(t[23]=[a("Source",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[24]||(t[24]=[a("Tier",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[25]||(t[25]=[a("维度",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[26]||(t[26]=[a("Articles",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[27]||(t[27]=[a("Valid",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[28]||(t[28]=[a("Signals",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[29]||(t[29]=[a("Events",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[30]||(t[30]=[a("Headlines",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[31]||(t[31]=[a("头条占比",-1)])]),_:1})]),_:1})]),_:1}),o(y,null,{default:l(()=>[(h(!0),D(G,null,le(ee.value.rows,r=>(h(),B(e(K),{key:r.source_id},{default:l(()=>[o(e(C),null,{default:l(()=>[a(c(r.name),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.tier),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.dimension),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.articles),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.valid),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.signals),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.events),1)]),_:2},1024),o(e(C),null,{default:l(()=>[o(e(ie),{type:r.headlines>0?"success":"default",size:"small"},{default:l(()=>[a(c(r.headlines),1)]),_:2},1032,["type"])]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.headline_share)+"%",1)]),_:2},1024)]),_:2},1024))),128))]),_:1})]),_:1})):(h(),B(e(he),{key:1,description:"今日无来源维度数据",size:"small"})),ee.value.note?(h(),B(e(de),{key:2,type:"default",class:"mt",title:ee.value.note||""},null,8,["title"])):se("",!0)]),_:1}),o(e(Y),{title:"3. Data Quality（数据质量）",class:"section"},{default:l(()=>[o(e(ne),{align:"center",justify:"space-between"},{default:l(()=>[o(e(F),{label:"Data Quality Score",value:N.value.score!=null?N.value.score+" / 100":"—"},null,8,["value"]),o(e(_e),{type:"dashboard",percentage:N.value.score||0,color:p(N.value.score||0)==="success"?"#18a058":p(N.value.score||0)==="warning"?"#f0a020":"#d03050",height:80},null,8,["percentage","color"])]),_:1}),N.value.content_warning?(h(),B(e(de),{key:0,type:"warning",class:"mt",title:N.value.note},null,8,["title"])):N.value.note?(h(),B(e(de),{key:1,type:"info",class:"mt",title:N.value.note},null,8,["title"])):se("",!0),N.value.completion?(h(),B(e(ue),{key:2,"single-line":!1,size:"small",class:"mt"},{default:l(()=>[o(e(ce),null,{default:l(()=>[o(e(K),null,{default:l(()=>[o(e(_),null,{default:l(()=>[...t[32]||(t[32]=[a("字段",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[33]||(t[33]=[a("完成率",-1)])]),_:1})]),_:1})]),_:1}),o(y,null,{default:l(()=>[(h(!0),D(G,null,le(N.value.completion,(r,U)=>(h(),B(e(K),{key:U},{default:l(()=>[o(e(C),null,{default:l(()=>[a(c(U),1)]),_:2},1024),o(e(C),null,{default:l(()=>[o(e(ie),{type:p(r),size:"small"},{default:l(()=>[a(c(r)+"%",1)]),_:2},1032,["type"])]),_:2},1024)]),_:2},1024))),128))]),_:1})]),_:1})):se("",!0)]),_:1}),o(e(Y),{title:"4. Editorial Intelligence（编辑智能）",class:"section"},{default:l(()=>[o(e(F),{label:"编辑智能覆盖",value:(q.value.editorial_coverage!=null?q.value.editorial_coverage:0)+"%"},null,8,["value"]),o(e(Ce),{"title-placement":"left"},{default:l(()=>[...t[34]||(t[34]=[a("Top Intelligence",-1)])]),_:1}),q.value.top_intelligence&&q.value.top_intelligence.length?(h(),B(e(ye),{key:0},{default:l(()=>[(h(!0),D(G,null,le(q.value.top_intelligence,(r,U)=>(h(),B(e(ze),{key:U},{default:l(()=>[o(te,{title:`${U+1}. ${r.title}`,description:`评分 ${r.score} · ${r.source} · ${r.tier} · ${r.dimension}`},null,8,["title","description"])]),_:2},1024))),128))]),_:1})):(h(),B(e(he),{key:1,description:"暂无有效编辑评分",size:"small"})),o(e(de),{type:"default",class:"mt",title:q.value.note},null,8,["title"])]),_:1}),o(e(Y),{title:"7. Product Readiness（产品准备度）",class:"section"},{default:l(()=>[o(e(ne),{align:"center",justify:"space-between"},{default:l(()=>[oe("div",null,[o(e(F),{label:"Homepage Readiness",value:(E.value.score!=null?E.value.score:0)+" / 100"},null,8,["value"]),o(e(ie),{type:H(E.value.confidence_level),class:"mt"},{default:l(()=>[a(c(E.value.confidence_level||"—"),1)]),_:1},8,["type"])]),o(e(_e),{type:"dashboard",percentage:E.value.score||0,color:H(E.value.confidence_level)==="success"?"#18a058":H(E.value.confidence_level)==="warning"?"#f0a020":"#d03050",height:90},null,8,["percentage","color"])]),_:1}),o(e(Pe),{cols:4,"x-gap":12,class:"mt"},{default:l(()=>[o(e(ae),null,{default:l(()=>{var r;return[o(e(F),{label:"源覆盖",value:(((r=E.value.components)==null?void 0:r.source_coverage)||0)+"%"},null,8,["value"])]}),_:1}),o(e(ae),null,{default:l(()=>{var r;return[o(e(F),{label:"数据完整",value:(((r=E.value.components)==null?void 0:r.data_completeness)||0)+"%"},null,8,["value"])]}),_:1}),o(e(ae),null,{default:l(()=>{var r;return[o(e(F),{label:"编辑置信",value:(((r=E.value.components)==null?void 0:r.editorial_confidence)||0)+"%"},null,8,["value"])]}),_:1}),o(e(ae),null,{default:l(()=>{var r;return[o(e(F),{label:"故事密度",value:(((r=E.value.components)==null?void 0:r.story_density)||0)+"%"},null,8,["value"])]}),_:1})]),_:1}),o(e(J),{depth:"3",class:"mt block"},{default:l(()=>[a("发现故事 "+c(E.value.stories_discovered)+" · 首页候选 "+c(E.value.homepage_candidates),1)]),_:1})]),_:1}),o(e(Y),{title:"8. Improvement Recommendations（改进建议）",class:"section"},{default:l(()=>[o(e(ye),null,{default:l(()=>[(h(!0),D(G,null,le(ve.value,(r,U)=>(h(),B(e(ze),{key:U},{default:l(()=>[o(e(ne),{align:"center"},{default:l(()=>[o(e(ie),{type:S(r.severity),size:"small"},{default:l(()=>[a(c(r.severity),1)]),_:2},1032,["type"]),oe("div",null,[o(e(J),{strong:""},{default:l(()=>[a(c(r.finding),1)]),_:2},1024),oe("div",null,[o(e(J),{depth:"3"},{default:l(()=>[a("行动："+c(r.action),1)]),_:2},1024)])])]),_:2},1024)]),_:2},1024))),128))]),_:1})]),_:1}),o(e(Y),{title:"9. Human Review Notes（人工编辑备注）",class:"section"},{default:l(()=>[Q.value.count?(h(),D(G,{key:0},[o(e(ne),{align:"center",justify:"space-between"},{default:l(()=>[o(e(F),{label:"反馈数",value:Q.value.count},null,8,["value"]),o(e(F),{label:"同意率",value:(Q.value.agreement_rate!=null?Q.value.agreement_rate:"—")+"%"},null,8,["value"])]),_:1}),o(e(Ce),{"title-placement":"left"},{default:l(()=>[...t[35]||(t[35]=[a("Samples",-1)])]),_:1}),o(e(ye),null,{default:l(()=>[(h(!0),D(G,null,le(Q.value.samples,r=>(h(),B(e(ze),{key:r.id},{default:l(()=>[o(e(ne),{align:"center",wrap:!1},{default:l(()=>[o(e(ie),{type:L(r.agreed),size:"small"},{default:l(()=>[a(c(r.agreed?"同意":"反驳"),1)]),_:2},1032,["type"]),oe("div",null,[o(e(J),{strong:""},{default:l(()=>[a("["+c(r.feedback_level)+"] 系统："+c(r.system_pick||"(未记录)"),1)]),_:2},1024),oe("div",null,[o(e(J),{depth:"3"},{default:l(()=>[a("人工："+c(r.human_pick||"—"),1)]),_:2},1024)]),r.human_reason?(h(),D("div",Po,[o(e(J),{depth:"3"},{default:l(()=>[a("理由："+c(r.human_reason),1)]),_:2},1024)])):se("",!0),r.disagreement_category?(h(),D("div",$o,[o(e(J),{depth:"3"},{default:l(()=>[a("类别："+c(r.disagreement_category),1)]),_:2},1024)])):se("",!0)])]),_:2},1024)]),_:2},1024))),128))]),_:1})],64)):(h(),B(e(he),{key:1,description:"今日暂无人工编辑反馈",size:"small"})),o(e(de),{type:"default",class:"mt",title:Q.value.note||"建议每日晨会记录对系统判断的同意/反驳（目标同意率 >70%）。"},null,8,["title"])]),_:1}),o(e(Y),{title:"历史趋势（近 30 天）",class:"section"},{default:l(()=>[o(e(ue),{"single-line":!1,size:"small"},{default:l(()=>[o(e(ce),null,{default:l(()=>[o(e(K),null,{default:l(()=>[o(e(_),null,{default:l(()=>[...t[36]||(t[36]=[a("日期",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[37]||(t[37]=[a("首页准备度",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[38]||(t[38]=[a("数据质量",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[39]||(t[39]=[a("采集文章",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[40]||(t[40]=[a("智能产出率",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[41]||(t[41]=[a("编辑覆盖",-1)])]),_:1}),o(e(_),null,{default:l(()=>[...t[42]||(t[42]=[a("建议数",-1)])]),_:1})]),_:1})]),_:1}),o(y,null,{default:l(()=>[(h(!0),D(G,null,le(v.value,r=>(h(),B(e(K),{key:r.date,style:{cursor:"pointer"},onClick:U=>z(r.date)},{default:l(()=>[o(e(C),null,{default:l(()=>[a(c(r.date),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.readiness_score!=null?r.readiness_score:"—"),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.data_quality_score!=null?r.data_quality_score:"—"),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.coverage_articles!=null?r.coverage_articles:"—"),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.intelligence_yield_rate!=null?r.intelligence_yield_rate+"%":"—"),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.editorial_coverage!=null?r.editorial_coverage+"%":"—"),1)]),_:2},1024),o(e(C),null,{default:l(()=>[a(c(r.recommendations_count),1)]),_:2},1024)]),_:2},1032,["onClick"]))),128))]),_:1})]),_:1})]),_:1})],64)):(h(),B(e(he),{key:0,description:"暂无报告，点击「生成今日报告」",class:"empty"}))]),_:1},8,["show"])])}}},Fo=Qe(Ro,[["__scopeId","data-v-1027a19f"]]);export{Fo as default};
