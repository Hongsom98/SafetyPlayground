from selenium import webdriver
import pandas as pd

driver = webdriver.Chrome("D:/chromedriver")
driver.get("http://race.kra.co.kr/raceScore/scoretablePeriodScoreList.do")
driver.find_element_by_xpath("//button[@type='button']//span[contains(text(),'기간별검색')]").click()
driver.find_element_by_xpath("//select[@id='arg_Year1']/option[text()='2020']").click()
driver.find_element_by_xpath("//select[@name='arg_Mon1']/option[text()='03']").click()
driver.find_element_by_xpath("//select[@name='arg_Day1']/option[text()='01']").click()

driver.find_element_by_xpath("//select[@id='arg_Year2']/option[text()='2020']").click()
driver.find_element_by_xpath("//select[@name='arg_Mon2']/option[text()='08']").click()
driver.find_element_by_xpath("//select[@name='arg_Day2']/option[text()='08']").click()

driver.find_element_by_xpath("//button[@type='button']//span[contains(text(),'검색')]").click()
length = len(driver.find_elements_by_xpath("//table//td[@class='alignL']//a"))

AddData = {}
count = 0
while True:
    try:
        for i in range(length):
            find_as = driver.find_elements_by_xpath("//table//td[@class='alignL']//a")
            find_as[i].click()

            to_add_text = driver.find_element_by_xpath("//div[@class='tableType1']").text.split()
            print(to_add_text)
            columns = [['순위', '마번', '마명', '산지', '성별', '연령', '중량', '기수명', '조교사명', '마주명', '마체중', '단승', '연승', '장구현황'],
                       ['구간별순위', 'S-1F', '1코너', '2코너', '3코너', 'G-3F', '4코너', 'G-1F', '경주기록'],
                       ['날짜', '날씨', '주로상태', '등급', '거리']]
            contents_s = []

            add_num = 0
            for idx, k in enumerate(driver.find_elements_by_xpath("//div[@class='tableType2']//tbody")[:2]):
                rows = k.find_elements_by_css_selector("tr")
                rows_contents = []
                for row in rows:
                    contents = row.find_elements_by_css_selector("td")
                    contents_text = [content.text for content in contents]

                    if idx == 0:
                        if contents_text[0] == '':
                            continue
                        else:
                            add_num += 1
                            del contents_text[7]
                            del contents_text[10]
                            contents_text[10] = contents_text[10][:3]
                    if idx == 1:
                        if contents_text[0] == '':
                            continue
                        else:
                            del contents_text[0]
                            del contents_text[0]
                            del contents_text[-2]
                            del contents_text[-2]

                    rows_contents.append(contents_text)

                contents_s.append(pd.DataFrame(rows_contents, columns=columns[idx]))
            to_contents = []
            for j in range(add_num):
                List = []
                List.append(to_add_text[0] + to_add_text[1] + to_add_text[2] + to_add_text[3])
                List.append(to_add_text[8])
                List.append(to_add_text[9])
                if to_add_text[16] == '연령오픈':
                    List.append(to_add_text[11])
                    List.append(to_add_text[12])
                else:
                    List.append(to_add_text[12])
                    List.append(to_add_text[13])
                to_contents.append(List)
            contents_s.append(pd.DataFrame(to_contents, columns=columns[2]))
            total_data = pd.concat([contents_s[0], contents_s[1], contents_s[2]], axis=1, ignore_index=False)
            count += 1
            total_data.to_csv("D:/csv/서울경마" + str(count) + '.csv', encoding='ms949')
            driver.execute_script("window.history.go(-1)")

        driver.find_element_by_xpath("//button[@type='button']//span[contains(text(),'다음')]").click()
    except:
        print("끝")
        break
