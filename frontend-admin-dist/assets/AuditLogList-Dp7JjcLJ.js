import{E as re,F as R,s as z,y as o,aa as le,A as V,C as q,H as ae,I as ne,d as Z,b3 as ie,m as h,b6 as se,L as de,O as ee,P as ce,p as U,U as H,aq as te,Q as pe,c as W,a as I,e as s,w as b,g as n,ar as ue,au as be,r as _,o as J,j as ge,B as F,as as P,l as G,aj as me,ap as N}from"./index-CRYXIsvh.js";import{_ as he}from"./_plugin-vue_export-helper-DlAUqK2U.js";import{S as ve}from"./SearchOutlined-qlFj0j2H.js";import{g as fe,u as ye,N as Q,a as X}from"./Space-DOsY5xaG.js";import{u as xe}from"./use-message-BppchCHs.js";import{N as we}from"./Input-BZv5i8Eu.js";import{N as Ce}from"./Select-DtSLODmb.js";import{N as Se}from"./DataTable-IiJICXKr.js";import{N as ze}from"./Pagination-CW6DKD64.js";import"./Suffix-r3DeWvWw.js";import"./Popover-CB8JeE3n.js";import"./format-length-B-p6aW7q.js";import"./Tooltip-LbMNDyVw.js";import"./Dropdown-FEeEDxR3.js";import"./Icon-B4ktjwSh.js";import"./create-ref-setter-C4J8sofl.js";import"./download-C2161hUv.js";function Y(r,y="default",f=[]){const{children:g}=r;if(g!==null&&typeof g=="object"&&!Array.isArray(g)){const d=g[y];if(typeof d=="function")return d()}return f}const _e={thPaddingBorderedSmall:"8px 12px",thPaddingBorderedMedium:"12px 16px",thPaddingBorderedLarge:"16px 24px",thPaddingSmall:"0",thPaddingMedium:"0",thPaddingLarge:"0",tdPaddingBorderedSmall:"8px 12px",tdPaddingBorderedMedium:"12px 16px",tdPaddingBorderedLarge:"16px 24px",tdPaddingSmall:"0 0 8px 0",tdPaddingMedium:"0 0 12px 0",tdPaddingLarge:"0 0 16px 0"};function Pe(r){const{tableHeaderColor:y,textColor2:f,textColor1:g,cardColor:d,modalColor:v,popoverColor:x,dividerColor:m,borderRadius:i,fontWeightStrong:p,lineHeight:u,fontSizeSmall:a,fontSizeMedium:w,fontSizeLarge:C}=r;return Object.assign(Object.assign({},_e),{lineHeight:u,fontSizeSmall:a,fontSizeMedium:w,fontSizeLarge:C,titleTextColor:g,thColor:R(d,y),thColorModal:R(v,y),thColorPopover:R(x,y),thTextColor:g,thFontWeight:p,tdTextColor:f,tdColor:d,tdColorModal:v,tdColorPopover:x,borderColor:R(d,m),borderColorModal:R(v,m),borderColorPopover:R(x,m),borderRadius:i})}const ke={common:re,self:Pe},$e=z([o("descriptions",{fontSize:"var(--n-font-size)"},[o("descriptions-separator",`
 display: inline-block;
 margin: 0 8px 0 2px;
 `),o("descriptions-table-wrapper",[o("descriptions-table",[o("descriptions-table-row",[o("descriptions-table-header",{padding:"var(--n-th-padding)"}),o("descriptions-table-content",{padding:"var(--n-td-padding)"})])])]),le("bordered",[o("descriptions-table-wrapper",[o("descriptions-table",[o("descriptions-table-row",[z("&:last-child",[o("descriptions-table-content",{paddingBottom:0})])])])])]),V("left-label-placement",[o("descriptions-table-content",[z("> *",{verticalAlign:"top"})])]),V("left-label-align",[z("th",{textAlign:"left"})]),V("center-label-align",[z("th",{textAlign:"center"})]),V("right-label-align",[z("th",{textAlign:"right"})]),V("bordered",[o("descriptions-table-wrapper",`
 border-radius: var(--n-border-radius);
 overflow: hidden;
 background: var(--n-merged-td-color);
 border: 1px solid var(--n-merged-border-color);
 `,[o("descriptions-table",[o("descriptions-table-row",[z("&:not(:last-child)",[o("descriptions-table-content",{borderBottom:"1px solid var(--n-merged-border-color)"}),o("descriptions-table-header",{borderBottom:"1px solid var(--n-merged-border-color)"})]),o("descriptions-table-header",`
 font-weight: 400;
 background-clip: padding-box;
 background-color: var(--n-merged-th-color);
 `,[z("&:not(:last-child)",{borderRight:"1px solid var(--n-merged-border-color)"})]),o("descriptions-table-content",[z("&:not(:last-child)",{borderRight:"1px solid var(--n-merged-border-color)"})])])])])]),o("descriptions-header",`
 font-weight: var(--n-th-font-weight);
 font-size: 18px;
 transition: color .3s var(--n-bezier);
 line-height: var(--n-line-height);
 margin-bottom: 16px;
 color: var(--n-title-text-color);
 `),o("descriptions-table-wrapper",`
 transition:
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `,[o("descriptions-table",`
 width: 100%;
 border-collapse: separate;
 border-spacing: 0;
 box-sizing: border-box;
 `,[o("descriptions-table-row",`
 box-sizing: border-box;
 transition: border-color .3s var(--n-bezier);
 `,[o("descriptions-table-header",`
 font-weight: var(--n-th-font-weight);
 line-height: var(--n-line-height);
 display: table-cell;
 box-sizing: border-box;
 color: var(--n-th-text-color);
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `),o("descriptions-table-content",`
 vertical-align: top;
 line-height: var(--n-line-height);
 display: table-cell;
 box-sizing: border-box;
 color: var(--n-td-text-color);
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 `,[q("content",`
 transition: color .3s var(--n-bezier);
 display: inline-block;
 color: var(--n-td-text-color);
 `)]),q("label",`
 font-weight: var(--n-th-font-weight);
 transition: color .3s var(--n-bezier);
 display: inline-block;
 margin-right: 14px;
 color: var(--n-th-text-color);
 `)])])])]),o("descriptions-table-wrapper",`
 --n-merged-th-color: var(--n-th-color);
 --n-merged-td-color: var(--n-td-color);
 --n-merged-border-color: var(--n-border-color);
 `),ae(o("descriptions-table-wrapper",`
 --n-merged-th-color: var(--n-th-color-modal);
 --n-merged-td-color: var(--n-td-color-modal);
 --n-merged-border-color: var(--n-border-color-modal);
 `)),ne(o("descriptions-table-wrapper",`
 --n-merged-th-color: var(--n-th-color-popover);
 --n-merged-td-color: var(--n-td-color-popover);
 --n-merged-border-color: var(--n-border-color-popover);
 `))]),oe="DESCRIPTION_ITEM_FLAG";function Ne(r){return typeof r=="object"&&r&&!Array.isArray(r)?r.type&&r.type[oe]:!1}const Be=Object.assign(Object.assign({},ee.props),{title:String,column:{type:Number,default:3},columns:Number,labelPlacement:{type:String,default:"top"},labelAlign:{type:String,default:"left"},separator:{type:String,default:":"},size:String,bordered:Boolean,labelClass:String,labelStyle:[Object,String],contentClass:String,contentStyle:[Object,String]}),De=Z({name:"Descriptions",props:Be,slots:Object,setup(r){const{mergedClsPrefixRef:y,inlineThemeDisabled:f,mergedComponentPropsRef:g}=de(r),d=U(()=>{var i,p;return r.size||((p=(i=g==null?void 0:g.value)===null||i===void 0?void 0:i.Descriptions)===null||p===void 0?void 0:p.size)||"medium"}),v=ee("Descriptions","-descriptions",$e,ke,r,y),x=U(()=>{const{bordered:i}=r,p=d.value,{common:{cubicBezierEaseInOut:u},self:{titleTextColor:a,thColor:w,thColorModal:C,thColorPopover:S,thTextColor:D,thFontWeight:E,tdTextColor:L,tdColor:l,tdColorModal:k,tdColorPopover:t,borderColor:e,borderColorModal:c,borderColorPopover:$,borderRadius:O,lineHeight:M,[H("fontSize",p)]:A,[H(i?"thPaddingBordered":"thPadding",p)]:T,[H(i?"tdPaddingBordered":"tdPadding",p)]:j}}=v.value;return{"--n-title-text-color":a,"--n-th-padding":T,"--n-td-padding":j,"--n-font-size":A,"--n-bezier":u,"--n-th-font-weight":E,"--n-line-height":M,"--n-th-text-color":D,"--n-td-text-color":L,"--n-th-color":w,"--n-th-color-modal":C,"--n-th-color-popover":S,"--n-td-color":l,"--n-td-color-modal":k,"--n-td-color-popover":t,"--n-border-radius":O,"--n-border-color":e,"--n-border-color-modal":c,"--n-border-color-popover":$}}),m=f?ce("descriptions",U(()=>{let i="";const{bordered:p}=r;return p&&(i+="a"),i+=d.value[0],i}),x,r):void 0;return{mergedClsPrefix:y,cssVars:f?void 0:x,themeClass:m==null?void 0:m.themeClass,onRender:m==null?void 0:m.onRender,compitableColumn:ye(r,["columns","column"]),inlineThemeDisabled:f,mergedSize:d}},render(){const r=this.$slots.default,y=r?ie(r()):[];y.length;const{contentClass:f,labelClass:g,compitableColumn:d,labelPlacement:v,labelAlign:x,mergedSize:m,bordered:i,title:p,cssVars:u,mergedClsPrefix:a,separator:w,onRender:C}=this;C==null||C();const S=y.filter(l=>Ne(l)),D={span:0,row:[],secondRow:[],rows:[]},L=S.reduce((l,k,t)=>{const e=k.props||{},c=S.length-1===t,$=["label"in e?e.label:Y(k,"label")],O=[Y(k)],M=e.span||1,A=l.span;l.span+=M;const T=e.labelStyle||e["label-style"]||this.labelStyle,j=e.contentStyle||e["content-style"]||this.contentStyle;if(v==="left")i?l.row.push(h("th",{class:[`${a}-descriptions-table-header`,g],colspan:1,style:T},$),h("td",{class:[`${a}-descriptions-table-content`,f],colspan:c?(d-A)*2+1:M*2-1,style:j},O)):l.row.push(h("td",{class:`${a}-descriptions-table-content`,colspan:c?(d-A)*2:M*2},h("span",{class:[`${a}-descriptions-table-content__label`,g],style:T},[...$,w&&h("span",{class:`${a}-descriptions-separator`},w)]),h("span",{class:[`${a}-descriptions-table-content__content`,f],style:j},O)));else{const K=c?(d-A)*2:M*2;l.row.push(h("th",{class:[`${a}-descriptions-table-header`,g],colspan:K,style:T},$)),l.secondRow.push(h("td",{class:[`${a}-descriptions-table-content`,f],colspan:K,style:j},O))}return(l.span>=d||c)&&(l.span=0,l.row.length&&(l.rows.push(l.row),l.row=[]),v!=="left"&&l.secondRow.length&&(l.rows.push(l.secondRow),l.secondRow=[])),l},D).rows.map(l=>h("tr",{class:`${a}-descriptions-table-row`},l));return h("div",{style:u,class:[`${a}-descriptions`,this.themeClass,`${a}-descriptions--${v}-label-placement`,`${a}-descriptions--${x}-label-align`,`${a}-descriptions--${m}-size`,i&&`${a}-descriptions--bordered`]},p||this.$slots.header?h("div",{class:`${a}-descriptions-header`},p||fe(this,"header")):null,h("div",{class:`${a}-descriptions-table-wrapper`},h("table",{class:`${a}-descriptions-table`},h("tbody",null,v==="top"&&h("tr",{class:`${a}-descriptions-table-row`,style:{visibility:"collapse"}},se(d*2,h("td",null))),L))))}}),Me={label:String,span:{type:Number,default:1},labelClass:String,labelStyle:[Object,String],contentClass:String,contentStyle:[Object,String]},B=Z({name:"DescriptionsItem",[oe]:!0,props:Me,slots:Object,render(){return null}});function Re(r){return te.get("/audit-logs",{params:r})}function Ie(r){return te.get(`/audit-logs/${r}`)}const Le={class:"audit-log-list"},Oe={key:0,class:"pagination-wrapper"},Ae={class:"json-pre"},Te={class:"json-pre"},je={__name:"AuditLogList",setup(r){const y=xe(),f=_(!1),g=_([]),d=_(0),v=_(1),x=_(20),m=_(""),i=_(null),p=_(!1),u=_(null),a=[{label:"全部操作",value:null},{label:"创建",value:"create"},{label:"更新",value:"update"},{label:"删除",value:"delete"},{label:"登录",value:"login"},{label:"登出",value:"logout"}],w={create:{text:"创建",type:"success"},update:{text:"更新",type:"warning"},delete:{text:"删除",type:"error"},login:{text:"登录",type:"info"},logout:{text:"登出",type:"default"}},C=[{title:"操作人",key:"operator",width:140},{title:"操作类型",key:"action",width:100,render:t=>{const e=w[t.action]||{};return h(X,{type:e.type||"default"},{default:()=>e.text||t.action})}},{title:"资源类型",key:"model_name",width:140},{title:"资源ID",key:"record_id",width:180,ellipsis:{tooltip:!0}},{title:"IP地址",key:"operator_ip",width:140},{title:"操作时间",key:"created_at",width:180,render:t=>new Date(t.created_at).toLocaleString()},{title:"操作",key:"actions",width:100,render:t=>h(F,{size:"small",type:"primary",text:!0,onClick:()=>L(t)},{default:()=>"详情"})}];async function S(){f.value=!0;try{const t={page:v.value,size:x.value};m.value&&(t.operator=m.value),i.value&&(t.action=i.value);const e=await Re(t);g.value=e.data.items,d.value=e.data.total}catch(t){y.error(t.message||"加载失败")}finally{f.value=!1}}function D(){v.value=1,S()}function E(){m.value="",i.value=null,v.value=1,S()}async function L(t){try{const e=await Ie(t.id);u.value=e.data,p.value=!0}catch(e){y.error(e.message||"加载详情失败")}}function l(t){v.value=t,S()}function k(t){if(!t)return"-";if(typeof t=="string")try{const e=JSON.parse(t);return JSON.stringify(e,null,2)}catch{return t}try{return JSON.stringify(t,null,2)}catch{return String(t)}}return pe(()=>{S()}),(t,e)=>(J(),W("div",Le,[e[9]||(e[9]=I("div",{class:"page-header"},[I("div",{class:"page-header-left"},[I("h2",{class:"page-title"},"审计日志"),I("p",{class:"page-desc"},"查看系统操作记录，追踪管理行为")])],-1)),s(n(ue),null,{default:b(()=>[s(n(Q),{vertical:"",size:16},{default:b(()=>[s(n(Q),{size:12,align:"center"},{default:b(()=>[s(n(we),{value:m.value,"onUpdate:value":e[0]||(e[0]=c=>m.value=c),placeholder:"搜索操作人...",style:{width:"240px"},clearable:"",onKeyup:ge(D,["enter"])},{prefix:b(()=>[s(n(ve))]),_:1},8,["value"]),s(n(Ce),{value:i.value,"onUpdate:value":[e[1]||(e[1]=c=>i.value=c),D],options:a,style:{width:"160px"}},null,8,["value"]),s(n(F),{type:"primary",onClick:D},{default:b(()=>[...e[6]||(e[6]=[P("搜索",-1)])]),_:1}),s(n(F),{onClick:E},{default:b(()=>[...e[7]||(e[7]=[P("重置",-1)])]),_:1})]),_:1}),s(n(Se),{columns:C,data:g.value,loading:f.value,bordered:!1,"scroll-x":"1100"},null,8,["data","loading"]),d.value>0?(J(),W("div",Oe,[s(n(ze),{page:v.value,"onUpdate:page":[e[2]||(e[2]=c=>v.value=c),l],"page-size":x.value,"onUpdate:pageSize":e[3]||(e[3]=c=>x.value=c),total:d.value,"page-sizes":[20,50,100],"show-size-picker":"","show-quick-jumper":""},null,8,["page","page-size","total"])])):G("",!0)]),_:1})]),_:1}),s(n(be),{show:p.value,"onUpdate:show":e[5]||(e[5]=c=>p.value=c),preset:"card",title:"审计日志详情",style:{width:"700px"}},{footer:b(()=>[s(n(F),{onClick:e[4]||(e[4]=c=>p.value=!1)},{default:b(()=>[...e[8]||(e[8]=[P("关闭",-1)])]),_:1})]),default:b(()=>[u.value?(J(),me(n(De),{key:0,column:1,bordered:""},{default:b(()=>[s(n(B),{label:"操作人"},{default:b(()=>[P(N(u.value.operator||"-"),1)]),_:1}),s(n(B),{label:"操作类型"},{default:b(()=>{var c;return[s(n(X),{type:((c=w[u.value.action])==null?void 0:c.type)||"default"},{default:b(()=>{var $;return[P(N((($=w[u.value.action])==null?void 0:$.text)||u.value.action),1)]}),_:1},8,["type"])]}),_:1}),s(n(B),{label:"资源类型"},{default:b(()=>[P(N(u.value.model_name||"-"),1)]),_:1}),s(n(B),{label:"资源ID"},{default:b(()=>[P(N(u.value.record_id||"-"),1)]),_:1}),s(n(B),{label:"IP地址"},{default:b(()=>[P(N(u.value.operator_ip||"-"),1)]),_:1}),s(n(B),{label:"操作时间"},{default:b(()=>[P(N(u.value.created_at?new Date(u.value.created_at).toLocaleString():"-"),1)]),_:1}),s(n(B),{label:"操作前数据"},{default:b(()=>[I("pre",Ae,N(k(u.value.before_data)),1)]),_:1}),s(n(B),{label:"操作后数据"},{default:b(()=>[I("pre",Te,N(k(u.value.after_data)),1)]),_:1})]),_:1})):G("",!0)]),_:1},8,["show"])]))}},rt=he(je,[["__scopeId","data-v-7545cca4"]]);export{rt as default};
