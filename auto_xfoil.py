from pathlib import Path
import pandas as pd
import xlwings as xw
import os
import subprocess
import numpy as np
from io import StringIO
import matplotlib.pyplot as plt

class automation:

    def __init__(self,airfoil_name,alpha,flap_deflection,x,y,Re,n_iter):
        self.foil_name = airfoil_name
        self.alpha = alpha
        self.flap_deflection = flap_deflection
        self.x = x
        self.y = y
        self.re = Re
        self.iter = n_iter
        self.excel_name = airfoil_name + str(flap_deflection)
        self.df = {} # darg_polar를 위한 빈 딕셔너리


    def airfoil_txt(self):


        # XFOIL input file 작성
        if os.path.exists(f"{self.excel_name}.txt"):
            os.remove(f"{self.excel_name}.txt")

        input_file = open("input_file.in", 'w')
        if 'naca' in self.foil_name:
            input_file.write(f'{self.foil_name}\n')

        else:
            input_file.write('load\n')
            input_file.write(f"{self.foil_name}\n")
        input_file.write('gdes\n')
        input_file.write('flap\n')
        input_file.write(f'{self.x}\n')
        input_file.write(f'{self.y}\n')
        input_file.write(f'{self.flap_deflection}\n')
        input_file.write('exec\n\n')
        input_file.write("PANE\n")
        input_file.write("OPER\n")
        input_file.write(f"Visc {self.re}\n")
        input_file.write("PACC\n")
        input_file.write(f"{self.excel_name}.txt\n\n")
        input_file.write(f"ITER {self.iter}\n")
        input_file.write(f"aseq {self.alpha[0]} {self.alpha[1]} {self.alpha[2]}\n")
        input_file.write("\n\n")
        input_file.write("quit\n")
        input_file.close()

        subprocess.call("xfoil.exe < input_file.in", shell=True)


    def txt_to_excell(self):
        # 디렉토리 설정
        current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
        input_dir = current_dir
        output_dir = current_dir / "OUTPUT" /"raw_excel_data"
        output_dir.mkdir(exist_ok=True, parents=True)
        files = list(input_dir.glob('*.txt'))
        key = self.excel_name

        with xw.App(visible=False) as app:
            wb = app.books.add()

            for file in files:
                if file.stem == key:
                    with open(file) as fil:
                        lines = fil.readlines()

                    lines1 = lines[:9]
                    lines2 = lines[10:-1]
                    csv_content1 = ''.join(lines1)
                    csv_content2 = ''.join(lines2)
                    csv_buffer1 = StringIO(csv_content1)
                    csv_buffer2 = StringIO(csv_content2)
                    df1 = pd.read_csv(csv_buffer1)
                    df2 = pd.read_csv(csv_buffer2, sep=r'\s+', engine='python', header=None)

                    wb.sheets[0].range("A1").options(index=False).value = df1.values
                    wb.sheets[0].range("A8").options(index=False).value = df2.values

            wb.sheets.add(name='Data plot 2', after=wb.sheets[0])
            sht = wb.sheets[1]
            sht.name = 'Data plot'

            y = pd.DataFrame()
            alpha = df2.iloc[2:, 0].astype(float)  # 숫자 형식으로 변환
            y['CL'] = df2.iloc[2:, 1].astype(float)
            y['CD'] = df2.iloc[2:, 2].astype(float)
            y['CDp'] = df2.iloc[2:, 3].astype(float)
            y['CM'] = df2.iloc[2:, 4].astype(float)
            y['TopXtr'] = df2.iloc[2:, 5].astype(float)
            y['BotXtr'] = df2.iloc[2:, 6].astype(float)

            figs = []

            # for i, col_name in enumerate(y):
            #     fig, ax = plt.subplots(figsize=(8, 6))
            #     ax.plot(alpha, y[col_name])
            #     ax.set_ylabel(col_name)
            #     ax.set_xlim(alpha.min() - 0.1, alpha.max() + 0.1)  # x축 범위를 0에서 20으로 설정
            #     ax.set_ylim(y[col_name].min() - 0.1, y[col_name].max() + 0.1)  # y축 범위 동적 설정
            #
            #     ax.set_xticks(np.linspace(alpha.min() - 0.1, alpha.max() + 0.1, 5))
            #     ax.set_yticks(np.linspace(y[col_name].min(), y[col_name].max(), 5))
            #
            #     figs.append(fig)

            fig1, ax = plt.subplots(figsize=(8, 6))
            ax.plot(y['CD'],y['CL'])
            ax.set_ylabel('CL')
            ax.set_xlabel('CD')
            ax.set_ylim(0,1.5)
            ax.set_xlim(0, 0.02)

            ax.set_xticks([0,0.005,0.01,0.015,0.02])
            ax.grid(True)

            figs.append(fig1)



            fig2,ax = plt.subplots(figsize=(8,6))
            ax.plot(alpha,y['CL'])
            ax.set_ylabel('CL')
            ax.set_xlabel('alpha')
            ax.set_ylim(y['CL'].min(),y['CL'].max())
            ax.set_xlim(alpha.min(),alpha.max())
            ax.grid(True)


            figs.append(fig2)

            sht.pictures.add(
                figs[0],
                name='matplotlib{0}'.format('dragploar'),
                update=True,
                left=sht.range('A1').left,
                top=sht.range('A1').top,
                height=200,
                width=300,
            )

            sht.pictures.add(
                figs[1],
                name='matplotlib{0}'.format('CL'),
                update=True,
                left=sht.range('G1').left,
                top=sht.range('A1').top,
                height=200,
                width=300,
            )



            wb.save(output_dir / f'{key}_Result.xlsx')
        return y

    def full_drag_polar(self,deflect_angles):

        # 디렉토리 설정
        for i in deflect_angles:
            current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
            input_dir = current_dir / 'OUTPUT' / 'raw_excel_data'
            output_dir = current_dir / "OUTPUT"
            output_dir.mkdir(exist_ok=True, parents=True)
            files = list(input_dir.glob('*.xlsx'))
            key = self.foil_name + str(i) +'_Result'



            for file in files:
                if file.stem == key:
                    with xw.Book(file) as fil:
                        sheet = fil.sheets[0]
                        self.df[f'CL_{i}'] = sheet.range('B10:B69').value
                        self.df[f'CD_{i}'] = sheet.range('C10:C69').value

        with xw.App(visible=False) as app:
            wb = app.books.add()

            wb.sheets.add(name='Data plot')
            sht = wb.sheets[0]
            sht.name = 'Data plot'
            fig, ax = plt.subplots(figsize=(8, 6))
            for i in deflect_angles:
                ax.plot(self.df[f'CD_{i}'], self.df[f'CL_{i}'],label=f'{i} deg flap')
            ax.set_ylabel('CL')
            ax.set_xlabel('CD')
            ax.set_ylim(0, 1.5)
            ax.set_xlim(0, 0.02)
            ax.set_xticks([0, 0.005, 0.01, 0.015, 0.02])
            plt.legend()
            plt.grid(True)


            sht.pictures.add(
                fig,
                name='matplotlib{0}'.format('CL'),
                update=True,
                left=sht.range('A1').left,
                top=sht.range('A1').top,
                height=200,
                width=300,
            )

            wb.save(output_dir / f'{self.foil_name}.xlsx')



