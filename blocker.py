from requests import session
ss = session()
# import các module cần dùng ở đây mình xài request
# reuquests để thực hiện các request lên sever facebook
def facebook_blocker(cookie,uid):
    # header + cookie để login vào fb
    headerFB = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    rq_1 = f'https://mbasic.facebook.com/privacy/touch/block/confirm/?bid={uid}&ret_cancel&source=profile'
    try:
        # trước tiên cần check xem cookie có thể vào được fb hay không đâu là dấu hiệu nhận biết login thành công => 
        # theo mình tìm hiểu thì có một id cạnh chữ đăng xuất nếu login thành công mình sẽ lấy nó làm dấu hiệu => "mbasic_logout_button"
        check_login_get_data = ss.get(rq_1,headers=headerFB)
        if check_login_get_data.status_code == 200:
            if 'mbasic_logout_button' in check_login_get_data.text:
                # Đăng nhập thành công => giờ thì lấy các data cần thiết để post lên sever fb
                fb_dtsg = check_login_get_data.text.split('name="fb_dtsg" value="')[1].split('" autocomplete="off"')[0]
                jazoest = check_login_get_data.text.split('name="jazoest" value="')[1].split('" autocomplete="off"')[0]
                data_post = {
                    'fb_dtsg': fb_dtsg,
                    'jazoest': jazoest,
                    'confirmed': 'Chặn'
                }
                link_block = 'https://mbasic.facebook.com/'+check_login_get_data.text.split('<form method="post" action="')[1].split('"><input type="hidden" name="fb_dtsg" value="')[0].replace('amp;','')
                print(link_block)
                rq_2 = 'https://mbasic.facebook.com/privacy/touch/block/confirm/?bid={uid}' #đây là url để block
                block_user = ss.post(link_block,headers=headerFB,data=data_post) #thường thì ở đây sau khi post để xem có block thành công hay không tỉ lệ chuẩn cũng không cao cho nên mình sẽ vào thẳng block list để check
                # giờ thì cần truy cập vào blocklist
                url_block_list = 'https://mbasic.facebook.com/privacy/touch/block/?settings_tracking=mbasic_footer_link%3Asettings_3_0_pecs&_rdr'
                get_block_list = ss.get(url_block_list,headers=headerFB)
                if get_block_list.status_code == 200:
                    if uid in get_block_list.text:
                        print(f'{uid} ==> BLOCK SUCCESS')
                        # sau khi in ra mình muốn nó lưu lại file
                        with open('block_success.txt','a',encoding='utf-8') as saveFile:
                            saveFile.write(uid+'\n')
                    else:
                        print(f'{uid} ==> BLOCK FALSE')
                        with open('block_false.txt','a',encoding='utf-8') as saveFile:
                            saveFile.write(uid+'\n')
                else:
                    print(f'ERROR UNKNOWN => PLZ CHECK YOUR COOKIE AND TRY AGAIN ')
            else:
                print(f'LOGIN FALSE => PLZ CHECK YOUR COOKIE AND TRY AGAIN')
        else:
            print(f'LOGIN FALSE => PLZ CHECK YOUR COOKIE AND TRY AGAIN')
    except:
        print(f'LOGIN FALSE => PLZ CHECK YOUR COOKIE AND TRY AGAIN')