//dir_in = getDirectory("Choose the folder with your processed images");
dir_in= "C:/Users/heino/Desktop/marina_code/output/"

Table.create("image_data");
table_index = 0;

run("Bio-Formats Macro Extensions");
function processBioFormatFiles(currentDirectory) {
	fileList = getFileList(currentDirectory);
	for (file = 0; file < fileList.length; file++) {
		Ext.isThisType(currentDirectory + fileList[file], supportedFileFormat);
		if (supportedFileFormat=="true") {
			Ext.setId(currentDirectory + fileList[file]);
			Ext.getSeriesCount(seriesCount);
			for (series = 1; series <= seriesCount; series++) {
				run("Bio-Formats Importer", "open=[" + currentDirectory + fileList[file] + "] autoscale color_mode=Composite rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_"+series);
				
				raw_image_title = getTitle();
				run("Select All");
				getStatistics(area, mean, min, max, std, histogram);
							
				total_signal = area * mean;
				Table.set("file_name", table_index, fileList[file]);
				Table.set("full image mean",  table_index, mean);
				Table.set("full image area",  table_index, area);
				Table.set("full image max",  table_index, max);
				Table.set("full image signal (area*mean)", table_index, total_signal);
				table_index +=1;
				close("*");
			}
		//open any subfolders, and run the above code on their contents
		} else if (endsWith(fileList[file], "/")) {
			processBioFormatFiles(currentDirectory + fileList[file]);
		}
	}
}

processBioFormatFiles(dir_in);