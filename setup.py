from setuptools import setup

setup(
	name='pyreindent',
	version='0.1',
	scripts=['pyreindent.py'],
	package_data={"": ["*.rst"]},
	author='Anton Bernatskiy',
	author_email='abernats@uvm.edu',
	description='Freely switch between Python indentation styles',
	classifiers=[
	  'Development Status :: 4 - Beta',
	  'License :: OSI Approved :: MIT License',
	  'Programming Language :: Python :: 3',
	  'Topic :: Text Processing :: Filters'
	],
	url='https://github.com/abernatskiy/pyreindent',
	license='MIT',
	install_requires=['markdown']
)
