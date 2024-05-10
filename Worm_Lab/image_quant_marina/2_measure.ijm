//dir_in = getDirectory("Choose the folder with your processed images");
dir_in= "C:/Users/heino/Desktop/marina_code/output/"

//dir_out = getDirectory("Choose the folder to save ROI's to");
dir_ROI= "C:/Users/heino/Desktop/marina_code/ROI/"

Table.create("worm_data");
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
				roiManager("reset");
				run("Bio-Formats Importer", "open=[" + currentDirectory + fileList[file] + "] autoscale color_mode=Composite rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_"+series);
				
				//subtract the value of the background from the entire image
				run("Subtract...", "value=105");
				
				setMinAndMax(0, 300); //brighten the image for user (does not change measured pixel values)
				setLocation(0, 0); //move window to same spot for consistency with tracing
				setTool("freehand");
		
				waitForUser("Please outline the area you want to measure, then press ok");
				getStatistics(area, mean, min, max, std, histogram);
				roiManager("Add");
				roiManager("Save", "C:/Users/heino/Desktop/marina_code/ROIs/"+fileList[file]+".roi");
				close("*");
				
				//record values in table	
				total_signal = area * mean;
				Table.set("file_name", table_index, fileList[file]);
				Table.set("mean",  table_index, mean);
				Table.set("area",  table_index, area);
				Table.set("max",  table_index, max);
				Table.set("signal (area*mean)", table_index, total_signal);
				table_index +=1;
				
			}
		//open any subfolders, and run the above code on their contents
		} else if (endsWith(fileList[file], "/")) {
			processBioFormatFiles(currentDirectory + fileList[file]);
		}
	}
}

processBioFormatFiles(dir_in);