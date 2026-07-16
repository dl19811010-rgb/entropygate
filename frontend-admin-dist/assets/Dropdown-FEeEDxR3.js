import{p as ke,B as Ne,d as Ie,e as Re,h as le,r as Ke,N as ze,a as ce,c as Oe}from"./Popover-CB8JeE3n.js";import{be as Be,aO as Ae,aL as q,n as ie,bf as Te,bg as De,S as Fe,aJ as G,r as _,d as A,m as l,a3 as _e,E as He,a5 as Me,G as de,ac as X,M as H,ai as pe,Y as Le,ae as V,p as w,bh as fe,a0 as j,af as $e,aB as je,b7 as We,bi as Ee,bj as Ue,y as N,X as qe,s as $,aa as se,A as K,C as B,ag as Ge,L as Ve,O as he,P as Xe,a9 as te,t as z,U as F}from"./index-CRYXIsvh.js";import{N as Je}from"./Icon-B4ktjwSh.js";import{a as Ye}from"./use-message-BppchCHs.js";import{c as Ze}from"./create-ref-setter-C4J8sofl.js";function Qe(e={},o){const d=Ae({ctrl:!1,command:!1,win:!1,shift:!1,tab:!1}),{keydown:i,keyup:r}=e,n=a=>{switch(a.key){case"Control":d.ctrl=!0;break;case"Meta":d.command=!0,d.win=!0;break;case"Shift":d.shift=!0;break;case"Tab":d.tab=!0;break}i!==void 0&&Object.keys(i).forEach(b=>{if(b!==a.key)return;const v=i[b];if(typeof v=="function")v(a);else{const{stop:y=!1,prevent:x=!1}=v;y&&a.stopPropagation(),x&&a.preventDefault(),v.handler(a)}})},u=a=>{switch(a.key){case"Control":d.ctrl=!1;break;case"Meta":d.command=!1,d.win=!1;break;case"Shift":d.shift=!1;break;case"Tab":d.tab=!1;break}r!==void 0&&Object.keys(r).forEach(b=>{if(b!==a.key)return;const v=r[b];if(typeof v=="function")v(a);else{const{stop:y=!1,prevent:x=!1}=v;y&&a.stopPropagation(),x&&a.preventDefault(),v.handler(a)}})},f=()=>{(o===void 0||o.value)&&(q("keydown",document,n),q("keyup",document,u)),o!==void 0&&ie(o,a=>{a?(q("keydown",document,n),q("keyup",document,u)):(G("keydown",document,n),G("keyup",document,u))})};return Te()?(De(f),Fe(()=>{(o===void 0||o.value)&&(G("keydown",document,n),G("keyup",document,u))})):f(),Be(d)}function eo(e,o,d){const i=_(e.value);let r=null;return ie(e,n=>{r!==null&&window.clearTimeout(r),n===!0?d&&!d.value?i.value=!0:r=window.setTimeout(()=>{i.value=!0},o):i.value=!1}),i}const oo=A({name:"ChevronRight",render(){return l("svg",{viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg"},l("path",{d:"M5.64645 3.14645C5.45118 3.34171 5.45118 3.65829 5.64645 3.85355L9.79289 8L5.64645 12.1464C5.45118 12.3417 5.45118 12.6583 5.64645 12.8536C5.84171 13.0488 6.15829 13.0488 6.35355 12.8536L10.8536 8.35355C11.0488 8.15829 11.0488 7.84171 10.8536 7.64645L6.35355 3.14645C6.15829 2.95118 5.84171 2.95118 5.64645 3.14645Z",fill:"currentColor"}))}}),no={padding:"4px 0",optionIconSizeSmall:"14px",optionIconSizeMedium:"16px",optionIconSizeLarge:"16px",optionIconSizeHuge:"18px",optionSuffixWidthSmall:"14px",optionSuffixWidthMedium:"14px",optionSuffixWidthLarge:"16px",optionSuffixWidthHuge:"16px",optionIconSuffixWidthSmall:"32px",optionIconSuffixWidthMedium:"32px",optionIconSuffixWidthLarge:"36px",optionIconSuffixWidthHuge:"36px",optionPrefixWidthSmall:"14px",optionPrefixWidthMedium:"14px",optionPrefixWidthLarge:"16px",optionPrefixWidthHuge:"16px",optionIconPrefixWidthSmall:"36px",optionIconPrefixWidthMedium:"36px",optionIconPrefixWidthLarge:"40px",optionIconPrefixWidthHuge:"40px"};function to(e){const{primaryColor:o,textColor2:d,dividerColor:i,hoverColor:r,popoverColor:n,invertedColor:u,borderRadius:f,fontSizeSmall:a,fontSizeMedium:b,fontSizeLarge:v,fontSizeHuge:y,heightSmall:x,heightMedium:P,heightLarge:C,heightHuge:I,textColor3:S,opacityDisabled:k}=e;return Object.assign(Object.assign({},no),{optionHeightSmall:x,optionHeightMedium:P,optionHeightLarge:C,optionHeightHuge:I,borderRadius:f,fontSizeSmall:a,fontSizeMedium:b,fontSizeLarge:v,fontSizeHuge:y,optionTextColor:d,optionTextColorHover:d,optionTextColorActive:o,optionTextColorChildActive:o,color:n,dividerColor:i,suffixColor:d,prefixColor:d,optionColorHover:r,optionColorActive:Me(o,{alpha:.1}),groupHeaderTextColor:S,optionTextColorInverted:"#BBB",optionTextColorHoverInverted:"#FFF",optionTextColorActiveInverted:"#FFF",optionTextColorChildActiveInverted:"#FFF",colorInverted:u,dividerColorInverted:"#BBB",suffixColorInverted:"#BBB",prefixColorInverted:"#BBB",optionColorHoverInverted:o,optionColorActiveInverted:o,groupHeaderTextColorInverted:"#AAA",optionOpacityDisabled:k})}const ro=_e({name:"Dropdown",common:He,peers:{Popover:ke},self:to}),ae=de("n-dropdown-menu"),J=de("n-dropdown"),ue=de("n-dropdown-option"),ve=A({name:"DropdownDivider",props:{clsPrefix:{type:String,required:!0}},render(){return l("div",{class:`${this.clsPrefix}-dropdown-divider`})}}),io=A({name:"DropdownGroupHeader",props:{clsPrefix:{type:String,required:!0},tmNode:{type:Object,required:!0}},setup(){const{showIconRef:e,hasSubmenuRef:o}=H(ae),{renderLabelRef:d,labelFieldRef:i,nodePropsRef:r,renderOptionRef:n}=H(J);return{labelField:i,showIcon:e,hasSubmenu:o,renderLabel:d,nodeProps:r,renderOption:n}},render(){var e;const{clsPrefix:o,hasSubmenu:d,showIcon:i,nodeProps:r,renderLabel:n,renderOption:u}=this,{rawNode:f}=this.tmNode,a=l("div",Object.assign({class:`${o}-dropdown-option`},r==null?void 0:r(f)),l("div",{class:`${o}-dropdown-option-body ${o}-dropdown-option-body--group`},l("div",{"data-dropdown-option":!0,class:[`${o}-dropdown-option-body__prefix`,i&&`${o}-dropdown-option-body__prefix--show-icon`]},X(f.icon)),l("div",{class:`${o}-dropdown-option-body__label`,"data-dropdown-option":!0},n?n(f):X((e=f.title)!==null&&e!==void 0?e:f[this.labelField])),l("div",{class:[`${o}-dropdown-option-body__suffix`,d&&`${o}-dropdown-option-body__suffix--has-submenu`],"data-dropdown-option":!0})));return u?u({node:a,option:f}):a}});function re(e,o){return e.type==="submenu"||e.type===void 0&&e[o]!==void 0}function ao(e){return e.type==="group"}function me(e){return e.type==="divider"}function lo(e){return e.type==="render"}const be=A({name:"DropdownOption",props:{clsPrefix:{type:String,required:!0},tmNode:{type:Object,required:!0},parentKey:{type:[String,Number],default:null},placement:{type:String,default:"right-start"},props:Object,scrollable:Boolean},setup(e){const o=H(J),{hoverKeyRef:d,keyboardKeyRef:i,lastToggledSubmenuKeyRef:r,pendingKeyPathRef:n,activeKeyPathRef:u,animatedRef:f,mergedShowRef:a,renderLabelRef:b,renderIconRef:v,labelFieldRef:y,childrenFieldRef:x,renderOptionRef:P,nodePropsRef:C,menuPropsRef:I}=o,S=H(ue,null),k=H(ae),O=H(fe),E=w(()=>e.tmNode.rawNode),W=w(()=>{const{value:t}=x;return re(e.tmNode.rawNode,t)}),Y=w(()=>{const{disabled:t}=e.tmNode;return t}),Z=w(()=>{if(!W.value)return!1;const{key:t,disabled:p}=e.tmNode;if(p)return!1;const{value:g}=d,{value:T}=i,{value:ne}=r,{value:D}=n;return g!==null?D.includes(t):T!==null?D.includes(t)&&D[D.length-1]!==t:ne!==null?D.includes(t):!1}),Q=w(()=>i.value===null&&!f.value),ee=eo(Z,300,Q),oe=w(()=>!!(S!=null&&S.enteringSubmenuRef.value)),M=_(!1);j(ue,{enteringSubmenuRef:M});function L(){M.value=!0}function U(){M.value=!1}function R(){const{parentKey:t,tmNode:p}=e;p.disabled||a.value&&(r.value=t,i.value=null,d.value=p.key)}function s(){const{tmNode:t}=e;t.disabled||a.value&&d.value!==t.key&&R()}function c(t){if(e.tmNode.disabled||!a.value)return;const{relatedTarget:p}=t;p&&!le({target:p},"dropdownOption")&&!le({target:p},"scrollbarRail")&&(d.value=null)}function h(){const{value:t}=W,{tmNode:p}=e;a.value&&!t&&!p.disabled&&(o.doSelect(p.key,p.rawNode),o.doUpdateShow(!1))}return{labelField:y,renderLabel:b,renderIcon:v,siblingHasIcon:k.showIconRef,siblingHasSubmenu:k.hasSubmenuRef,menuProps:I,popoverBody:O,animated:f,mergedShowSubmenu:w(()=>ee.value&&!oe.value),rawNode:E,hasSubmenu:W,pending:V(()=>{const{value:t}=n,{key:p}=e.tmNode;return t.includes(p)}),childActive:V(()=>{const{value:t}=u,{key:p}=e.tmNode,g=t.findIndex(T=>p===T);return g===-1?!1:g<t.length-1}),active:V(()=>{const{value:t}=u,{key:p}=e.tmNode,g=t.findIndex(T=>p===T);return g===-1?!1:g===t.length-1}),mergedDisabled:Y,renderOption:P,nodeProps:C,handleClick:h,handleMouseMove:s,handleMouseEnter:R,handleMouseLeave:c,handleSubmenuBeforeEnter:L,handleSubmenuAfterEnter:U}},render(){var e,o;const{animated:d,rawNode:i,mergedShowSubmenu:r,clsPrefix:n,siblingHasIcon:u,siblingHasSubmenu:f,renderLabel:a,renderIcon:b,renderOption:v,nodeProps:y,props:x,scrollable:P}=this;let C=null;if(r){const O=(e=this.menuProps)===null||e===void 0?void 0:e.call(this,i,i.children);C=l(we,Object.assign({},O,{clsPrefix:n,scrollable:this.scrollable,tmNodes:this.tmNode.children,parentKey:this.tmNode.key}))}const I={class:[`${n}-dropdown-option-body`,this.pending&&`${n}-dropdown-option-body--pending`,this.active&&`${n}-dropdown-option-body--active`,this.childActive&&`${n}-dropdown-option-body--child-active`,this.mergedDisabled&&`${n}-dropdown-option-body--disabled`],onMousemove:this.handleMouseMove,onMouseenter:this.handleMouseEnter,onMouseleave:this.handleMouseLeave,onClick:this.handleClick},S=y==null?void 0:y(i),k=l("div",Object.assign({class:[`${n}-dropdown-option`,S==null?void 0:S.class],"data-dropdown-option":!0},S),l("div",pe(I,x),[l("div",{class:[`${n}-dropdown-option-body__prefix`,u&&`${n}-dropdown-option-body__prefix--show-icon`]},[b?b(i):X(i.icon)]),l("div",{"data-dropdown-option":!0,class:`${n}-dropdown-option-body__label`},a?a(i):X((o=i[this.labelField])!==null&&o!==void 0?o:i.title)),l("div",{"data-dropdown-option":!0,class:[`${n}-dropdown-option-body__suffix`,f&&`${n}-dropdown-option-body__suffix--has-submenu`]},this.hasSubmenu?l(Je,null,{default:()=>l(oo,null)}):null)]),this.hasSubmenu?l(Ne,null,{default:()=>[l(Ie,null,{default:()=>l("div",{class:`${n}-dropdown-offset-container`},l(Re,{show:this.mergedShowSubmenu,placement:this.placement,to:P&&this.popoverBody||void 0,teleportDisabled:!P},{default:()=>l("div",{class:`${n}-dropdown-menu-wrapper`},d?l(Le,{onBeforeEnter:this.handleSubmenuBeforeEnter,onAfterEnter:this.handleSubmenuAfterEnter,name:"fade-in-scale-up-transition",appear:!0},{default:()=>C}):C)}))})]}):null);return v?v({node:k,option:i}):k}}),so=A({name:"NDropdownGroup",props:{clsPrefix:{type:String,required:!0},tmNode:{type:Object,required:!0},parentKey:{type:[String,Number],default:null}},render(){const{tmNode:e,parentKey:o,clsPrefix:d}=this,{children:i}=e;return l($e,null,l(io,{clsPrefix:d,tmNode:e,key:e.key}),i==null?void 0:i.map(r=>{const{rawNode:n}=r;return n.show===!1?null:me(n)?l(ve,{clsPrefix:d,key:r.key}):r.isGroup?(je("dropdown","`group` node is not allowed to be put in `group` node."),null):l(be,{clsPrefix:d,tmNode:r,parentKey:o,key:r.key})}))}}),uo=A({name:"DropdownRenderOption",props:{tmNode:{type:Object,required:!0}},render(){const{rawNode:{render:e,props:o}}=this.tmNode;return l("div",o,[e==null?void 0:e()])}}),we=A({name:"DropdownMenu",props:{scrollable:Boolean,showArrow:Boolean,arrowStyle:[String,Object],clsPrefix:{type:String,required:!0},tmNodes:{type:Array,default:()=>[]},parentKey:{type:[String,Number],default:null}},setup(e){const{renderIconRef:o,childrenFieldRef:d}=H(J);j(ae,{showIconRef:w(()=>{const r=o.value;return e.tmNodes.some(n=>{var u;if(n.isGroup)return(u=n.children)===null||u===void 0?void 0:u.some(({rawNode:a})=>r?r(a):a.icon);const{rawNode:f}=n;return r?r(f):f.icon})}),hasSubmenuRef:w(()=>{const{value:r}=d;return e.tmNodes.some(n=>{var u;if(n.isGroup)return(u=n.children)===null||u===void 0?void 0:u.some(({rawNode:a})=>re(a,r));const{rawNode:f}=n;return re(f,r)})})});const i=_(null);return j(Ee,null),j(Ue,null),j(fe,i),{bodyRef:i}},render(){const{parentKey:e,clsPrefix:o,scrollable:d}=this,i=this.tmNodes.map(r=>{const{rawNode:n}=r;return n.show===!1?null:lo(n)?l(uo,{tmNode:r,key:r.key}):me(n)?l(ve,{clsPrefix:o,key:r.key}):ao(n)?l(so,{clsPrefix:o,tmNode:r,parentKey:e,key:r.key}):l(be,{clsPrefix:o,tmNode:r,parentKey:e,key:r.key,props:n.props,scrollable:d})});return l("div",{class:[`${o}-dropdown-menu`,d&&`${o}-dropdown-menu--scrollable`],ref:"bodyRef"},d?l(We,{contentClass:`${o}-dropdown-menu__content`},{default:()=>i}):i,this.showArrow?Ke({clsPrefix:o,arrowStyle:this.arrowStyle,arrowClass:void 0,arrowWrapperClass:void 0,arrowWrapperStyle:void 0}):null)}}),co=N("dropdown-menu",`
 transform-origin: var(--v-transform-origin);
 background-color: var(--n-color);
 border-radius: var(--n-border-radius);
 box-shadow: var(--n-box-shadow);
 position: relative;
 transition:
 background-color .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier);
`,[qe(),N("dropdown-option",`
 position: relative;
 `,[$("a",`
 text-decoration: none;
 color: inherit;
 outline: none;
 `,[$("&::before",`
 content: "";
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 `)]),N("dropdown-option-body",`
 display: flex;
 cursor: pointer;
 position: relative;
 height: var(--n-option-height);
 line-height: var(--n-option-height);
 font-size: var(--n-font-size);
 color: var(--n-option-text-color);
 transition: color .3s var(--n-bezier);
 `,[$("&::before",`
 content: "";
 position: absolute;
 top: 0;
 bottom: 0;
 left: 4px;
 right: 4px;
 transition: background-color .3s var(--n-bezier);
 border-radius: var(--n-border-radius);
 `),se("disabled",[K("pending",`
 color: var(--n-option-text-color-hover);
 `,[B("prefix, suffix",`
 color: var(--n-option-text-color-hover);
 `),$("&::before","background-color: var(--n-option-color-hover);")]),K("active",`
 color: var(--n-option-text-color-active);
 `,[B("prefix, suffix",`
 color: var(--n-option-text-color-active);
 `),$("&::before","background-color: var(--n-option-color-active);")]),K("child-active",`
 color: var(--n-option-text-color-child-active);
 `,[B("prefix, suffix",`
 color: var(--n-option-text-color-child-active);
 `)])]),K("disabled",`
 cursor: not-allowed;
 opacity: var(--n-option-opacity-disabled);
 `),K("group",`
 font-size: calc(var(--n-font-size) - 1px);
 color: var(--n-group-header-text-color);
 `,[B("prefix",`
 width: calc(var(--n-option-prefix-width) / 2);
 `,[K("show-icon",`
 width: calc(var(--n-option-icon-prefix-width) / 2);
 `)])]),B("prefix",`
 width: var(--n-option-prefix-width);
 display: flex;
 justify-content: center;
 align-items: center;
 color: var(--n-prefix-color);
 transition: color .3s var(--n-bezier);
 z-index: 1;
 `,[K("show-icon",`
 width: var(--n-option-icon-prefix-width);
 `),N("icon",`
 font-size: var(--n-option-icon-size);
 `)]),B("label",`
 white-space: nowrap;
 flex: 1;
 z-index: 1;
 `),B("suffix",`
 box-sizing: border-box;
 flex-grow: 0;
 flex-shrink: 0;
 display: flex;
 justify-content: flex-end;
 align-items: center;
 min-width: var(--n-option-suffix-width);
 padding: 0 8px;
 transition: color .3s var(--n-bezier);
 color: var(--n-suffix-color);
 z-index: 1;
 `,[K("has-submenu",`
 width: var(--n-option-icon-suffix-width);
 `),N("icon",`
 font-size: var(--n-option-icon-size);
 `)]),N("dropdown-menu","pointer-events: all;")]),N("dropdown-offset-container",`
 pointer-events: none;
 position: absolute;
 left: 0;
 right: 0;
 top: -4px;
 bottom: -4px;
 `)]),N("dropdown-divider",`
 transition: background-color .3s var(--n-bezier);
 background-color: var(--n-divider-color);
 height: 1px;
 margin: 4px 0;
 `),N("dropdown-menu-wrapper",`
 transform-origin: var(--v-transform-origin);
 width: fit-content;
 `),$(">",[N("scrollbar",`
 height: inherit;
 max-height: inherit;
 `)]),se("scrollable",`
 padding: var(--n-padding);
 `),K("scrollable",[B("content",`
 padding: var(--n-padding);
 `)])]),po={animated:{type:Boolean,default:!0},keyboard:{type:Boolean,default:!0},size:String,inverted:Boolean,placement:{type:String,default:"bottom"},onSelect:[Function,Array],options:{type:Array,default:()=>[]},menuProps:Function,showArrow:Boolean,renderLabel:Function,renderIcon:Function,renderOption:Function,nodeProps:Function,labelField:{type:String,default:"label"},keyField:{type:String,default:"key"},childrenField:{type:String,default:"children"},value:[String,Number]},fo=Object.keys(ce),ho=Object.assign(Object.assign(Object.assign({},ce),po),he.props),yo=A({name:"Dropdown",inheritAttrs:!1,props:ho,setup(e){const o=_(!1),d=Ye(z(e,"show"),o),i=w(()=>{const{keyField:s,childrenField:c}=e;return Oe(e.options,{getKey(h){return h[s]},getDisabled(h){return h.disabled===!0},getIgnored(h){return h.type==="divider"||h.type==="render"},getChildren(h){return h[c]}})}),r=w(()=>i.value.treeNodes),n=_(null),u=_(null),f=_(null),a=w(()=>{var s,c,h;return(h=(c=(s=n.value)!==null&&s!==void 0?s:u.value)!==null&&c!==void 0?c:f.value)!==null&&h!==void 0?h:null}),b=w(()=>i.value.getPath(a.value).keyPath),v=w(()=>i.value.getPath(e.value).keyPath),y=V(()=>e.keyboard&&d.value);Qe({keydown:{ArrowUp:{prevent:!0,handler:Q},ArrowRight:{prevent:!0,handler:Z},ArrowDown:{prevent:!0,handler:ee},ArrowLeft:{prevent:!0,handler:Y},Enter:{prevent:!0,handler:oe},Escape:W}},y);const{mergedClsPrefixRef:x,inlineThemeDisabled:P,mergedComponentPropsRef:C}=Ve(e),I=w(()=>{var s,c;return e.size||((c=(s=C==null?void 0:C.value)===null||s===void 0?void 0:s.Dropdown)===null||c===void 0?void 0:c.size)||"medium"}),S=he("Dropdown","-dropdown",co,ro,e,x);j(J,{labelFieldRef:z(e,"labelField"),childrenFieldRef:z(e,"childrenField"),renderLabelRef:z(e,"renderLabel"),renderIconRef:z(e,"renderIcon"),hoverKeyRef:n,keyboardKeyRef:u,lastToggledSubmenuKeyRef:f,pendingKeyPathRef:b,activeKeyPathRef:v,animatedRef:z(e,"animated"),mergedShowRef:d,nodePropsRef:z(e,"nodeProps"),renderOptionRef:z(e,"renderOption"),menuPropsRef:z(e,"menuProps"),doSelect:k,doUpdateShow:O}),ie(d,s=>{!e.animated&&!s&&E()});function k(s,c){const{onSelect:h}=e;h&&te(h,s,c)}function O(s){const{"onUpdate:show":c,onUpdateShow:h}=e;c&&te(c,s),h&&te(h,s),o.value=s}function E(){n.value=null,u.value=null,f.value=null}function W(){O(!1)}function Y(){L("left")}function Z(){L("right")}function Q(){L("up")}function ee(){L("down")}function oe(){const s=M();s!=null&&s.isLeaf&&d.value&&(k(s.key,s.rawNode),O(!1))}function M(){var s;const{value:c}=i,{value:h}=a;return!c||h===null?null:(s=c.getNode(h))!==null&&s!==void 0?s:null}function L(s){const{value:c}=a,{value:{getFirstAvailableNode:h}}=i;let t=null;if(c===null){const p=h();p!==null&&(t=p.key)}else{const p=M();if(p){let g;switch(s){case"down":g=p.getNext();break;case"up":g=p.getPrev();break;case"right":g=p.getChild();break;case"left":g=p.getParent();break}g&&(t=g.key)}}t!==null&&(n.value=null,u.value=t)}const U=w(()=>{const{inverted:s}=e,c=I.value,{common:{cubicBezierEaseInOut:h},self:t}=S.value,{padding:p,dividerColor:g,borderRadius:T,optionOpacityDisabled:ne,[F("optionIconSuffixWidth",c)]:D,[F("optionSuffixWidth",c)]:ge,[F("optionIconPrefixWidth",c)]:ye,[F("optionPrefixWidth",c)]:xe,[F("fontSize",c)]:Se,[F("optionHeight",c)]:Pe,[F("optionIconSize",c)]:Ce}=t,m={"--n-bezier":h,"--n-font-size":Se,"--n-padding":p,"--n-border-radius":T,"--n-option-height":Pe,"--n-option-prefix-width":xe,"--n-option-icon-prefix-width":ye,"--n-option-suffix-width":ge,"--n-option-icon-suffix-width":D,"--n-option-icon-size":Ce,"--n-divider-color":g,"--n-option-opacity-disabled":ne};return s?(m["--n-color"]=t.colorInverted,m["--n-option-color-hover"]=t.optionColorHoverInverted,m["--n-option-color-active"]=t.optionColorActiveInverted,m["--n-option-text-color"]=t.optionTextColorInverted,m["--n-option-text-color-hover"]=t.optionTextColorHoverInverted,m["--n-option-text-color-active"]=t.optionTextColorActiveInverted,m["--n-option-text-color-child-active"]=t.optionTextColorChildActiveInverted,m["--n-prefix-color"]=t.prefixColorInverted,m["--n-suffix-color"]=t.suffixColorInverted,m["--n-group-header-text-color"]=t.groupHeaderTextColorInverted):(m["--n-color"]=t.color,m["--n-option-color-hover"]=t.optionColorHover,m["--n-option-color-active"]=t.optionColorActive,m["--n-option-text-color"]=t.optionTextColor,m["--n-option-text-color-hover"]=t.optionTextColorHover,m["--n-option-text-color-active"]=t.optionTextColorActive,m["--n-option-text-color-child-active"]=t.optionTextColorChildActive,m["--n-prefix-color"]=t.prefixColor,m["--n-suffix-color"]=t.suffixColor,m["--n-group-header-text-color"]=t.groupHeaderTextColor),m}),R=P?Xe("dropdown",w(()=>`${I.value[0]}${e.inverted?"i":""}`),U,e):void 0;return{mergedClsPrefix:x,mergedTheme:S,mergedSize:I,tmNodes:r,mergedShow:d,handleAfterLeave:()=>{e.animated&&E()},doUpdateShow:O,cssVars:P?void 0:U,themeClass:R==null?void 0:R.themeClass,onRender:R==null?void 0:R.onRender}},render(){const e=(i,r,n,u,f)=>{var a;const{mergedClsPrefix:b,menuProps:v}=this;(a=this.onRender)===null||a===void 0||a.call(this);const y=(v==null?void 0:v(void 0,this.tmNodes.map(P=>P.rawNode)))||{},x={ref:Ze(r),class:[i,`${b}-dropdown`,`${b}-dropdown--${this.mergedSize}-size`,this.themeClass],clsPrefix:b,tmNodes:this.tmNodes,style:[...n,this.cssVars],showArrow:this.showArrow,arrowStyle:this.arrowStyle,scrollable:this.scrollable,onMouseenter:u,onMouseleave:f};return l(we,pe(this.$attrs,x,y))},{mergedTheme:o}=this,d={show:this.mergedShow,theme:o.peers.Popover,themeOverrides:o.peerOverrides.Popover,internalOnAfterLeave:this.handleAfterLeave,internalRenderBody:e,onUpdateShow:this.doUpdateShow,"onUpdate:show":void 0};return l(ze,Object.assign({},Ge(this.$props,fo),d),{trigger:()=>{var i,r;return(r=(i=this.$slots).default)===null||r===void 0?void 0:r.call(i)}})}});export{oo as C,yo as N,ro as d};
