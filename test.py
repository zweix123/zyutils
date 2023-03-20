import net_util, html_util, show_util

resp = net_util.get_resp("https://www.vnpy.com/docs/cn/gateway.html")
t = html_util.example_vnpy_interface(resp.text)
show_util.example_vnpy_interface(t)
