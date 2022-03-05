
from PIL import Image
import os
import math
import random
import pickle
from copy import deepcopy

# 读取图像
def GetImage(ori_img):
	img = Image.open(ori_img)
	color = []
	width, height = img.size
	for j in range(height):
		temp = []
		for i in range(width):
			r, g, b = img.getpixel((i, j))[:3]
			# 用来获取图像中某一点的像素的RGB颜色值，getpixel的参数是一个坐标点。
			gr = (r+g+b)//3

			temp.append([gr, gr, gr])
		color.append(temp)
	return color, img.size
			# 返回color表，包含每个像素点RGB值


# 初始化
def RandGenes(size):
	width, height = size
	genes = []
	for i in range(100):
		gene = []
		for j in range(height):
			temp = []
			for i in range(width):
				r = random.randint(0, 255)
				g = random.randint(0, 255)
				b = random.randint(0, 255)
				gr = (r+g+b)//3

				temp.append([gr, gr, gr])
			gene.append(temp)
		genes.append([gene, 0])
	return genes



# 计算适应度
def CalcFitness(genes, target):
	for k, gene in enumerate(genes):
		count1 = 0
		count2 = 0
		for i, row in enumerate(gene[0]):
			for j, col in enumerate(row):
				t_r, t_g, t_b= target[i][j]
				r, g, b= col
				count1 += (abs(t_r-r) + abs(t_g-g) + abs(t_b-b))
				#count2 += (abs(t_r) + abs(t_g)+ abs(t_b))
		genes[k][1] = (count1//2700)
		#genes[k][2] = (count2-count1)//count2
	genes.sort(key = lambda x: x[1])
	return genes



# 变异
def Variation(genes):
	rate = 0.5
	for k, gene in enumerate(genes):
		for i, row in enumerate(gene[0]):
			for j, col in enumerate(row):
				if random.random() < rate:
					tp=gene[1]//10
					a = [-1, 1][random.randint(0, 1)] * random.randint(0,tp)
					b = [-1, 1][random.randint(0, 1)] * random.randint(0,tp)
					c = [-1, 1][random.randint(0, 1)] * random.randint(0,tp)
					genes[k][0][i][j][0] += a
					genes[k][0][i][j][1] += b
					genes[k][0][i][j][2] += c
	return genes




# 交叉
def Merge(gene1, gene2, size):
	width, height = size
	y = random.randint(0, width-1)
	x = random.randint(0, height-1)
	new_gene = deepcopy(gene1[0][:x])
	new_gene = [new_gene, 0]
	new_gene[0][x:] = deepcopy(gene2[0][x:])
	new_gene[0][x][:y] = deepcopy(gene1[0][x][:y])
	return new_gene



# 自然选择
def Select(genes, size):
	seek = len(genes) * 2 // 3
	i = 0
	j = seek + 1
	while i < seek:
		genes[j] = Merge(genes[i], genes[i+1], size)
		j += 1
		i += 2
	return genes




# 保存生成的图片
def SavePic(gene, generation, ori_img):
	gene = gene[0]
	img = Image.open(ori_img)
	for j, row in enumerate(gene):
		for i, col in enumerate(row):
			r, g, b= col
			gr = (r+g+b)//3
			img.putpixel((i, j), (gr, gr, gr))
	img.save("{}.png".format(generation))







# 备份
def SaveData(data, backup):
	print('[INFO]: Save data to {}...'.format(backup))
	with open(backup, 'wb') as f:
		pickle.dump(data, f)
	f.close()



# 读取备份
def ReadData(backup):
	print('[INFO]: Read data from {}...'.format(backup))
	with open(backup, 'rb') as f:
		data = pickle.load(f)
		genes = data['genes']
		generation = data['generation']
	f.close()
	return genes, generation







# 运行

def run(ori_img, backup, resume=False):
	data, size = GetImage(ori_img)
	if resume:
		genes, generation = ReadData(backup)
	else:
		genes = RandGenes(size)
		generation = 0
	while True:
		genes = Variation(genes)
		genes = CalcFitness(genes, data)
		genes = Select(genes, size)
		generation += 1
		if generation % 50 == 0:
			SaveData({'gene`在这里插入代码片`s': genes, 'generation': generation}, backup)

			SavePic(genes[0], generation, ori_img)

		print('<Generation>: {}, <BestFit-Top3>: {:.4f} {:.4f} {:.4f}'.format(generation,228-2.3*(genes[0][1]), 228-2.3(genes[1][1]), 228-2.3*(genes[2][1])))


if __name__ == '__main__':
	# 备份
	backup = 'backup.tmp'
	# 原始图像
	ori_img = './test.png'
	# resume为True则读取备份文件，在其基础上进行自然选择，交叉变异
	run(ori_img, backup, resume=False)


