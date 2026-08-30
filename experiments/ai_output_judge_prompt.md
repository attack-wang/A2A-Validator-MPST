你是旅行规划实验的独立输出质量评价器。请只依据“最终回复”中明确出现的信息进行判断，不补充常识，不推断未写出的内容，也不评价文风。

依次判断以下六项是否满足：

1. transport：同时给出去程和返程的具体高铁车次或航班信息，并与任务日期一致。
2. hotel：给出明确酒店名称以及三晚住宿安排或相应入住、离店日期。
3. tickets：给出行程中主要景点及其门票价格、预约或购票信息。
4. weather：说明旅行期间的天气，并体现天气与室内、户外行程安排之间的对应关系。
5. daily_routes：逐日给出酒店与景点之间的市内交通方式，并包含起终点、换乘或路线以及费用信息。
6. budget：汇总跨城交通、住宿、门票和市内交通等费用，给出两位成人的总费用、人均费用以及是否超出预算。

每项只能输出 true 或 false。evidence 必须摘录或概括最终回复中的直接证据；不满足时说明缺失内容。只返回一个合法 JSON 对象，不要输出 Markdown 代码块或其他文字：

{
  "transport": {"satisfied": false, "evidence": "", "reason": ""},
  "hotel": {"satisfied": false, "evidence": "", "reason": ""},
  "tickets": {"satisfied": false, "evidence": "", "reason": ""},
  "weather": {"satisfied": false, "evidence": "", "reason": ""},
  "daily_routes": {"satisfied": false, "evidence": "", "reason": ""},
  "budget": {"satisfied": false, "evidence": "", "reason": ""}
}

最终回复如下：

---
{final_output}
---
