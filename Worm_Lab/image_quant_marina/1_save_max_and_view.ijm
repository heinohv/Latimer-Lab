//dir_in = getDirectory("Choose the folder with your unprocessed images");
dir_in= "C:/Users/heino/Desktop/marina_code/input/"

//dir_out = getDirectory("Choose the folder to save max projections to");
dir_out= "C:/Users/heino/Desktop/marina_code/output/"

//dir_out = getDirectory("Choose the folder to save edited images for viewing (NOT FOR QUANTIFICATION)");
dir_view= "C:/Users/heino/Desktop/marina_code/view/"

run("Bio-Formats Macro Extensions");
function processBioFormatFiles(currentDirectory) {
	fileList = getFileList(currentDirectory);
	
	Table.create("image_data");
	table_index = 0;
	
	for (file = 0; file < fileList.length; file++) {
		Ext.isThisType(currentDirectory + fileList[file], supportedFileFormat);
		if (supportedFileFormat=="true") {
			Ext.setId(currentDirectory + fileList[file]);
			Ext.getSeriesCount(seriesCount);
			for (series = 1; series <= seriesCount; series++) {
				run("Bio-Formats Importer", "open=[" + currentDirectory + fileList[file] + "] autoscale color_mode=Composite rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_"+series);
				//CODE TO APPLY TO IMAGE GOES HERE
				save_ch_2_max();
				
			}
		//open any subfolders, and run the above code on their contents
		} else if (endsWith(fileList[file], "/")) {
			processBioFormatFiles(currentDirectory + fileList[file]);
		}
	}
}

function save_ch_2_max() { 
	run("Split Channels");
	run("Tile");
	window_names = newArray();
	for (i = 1; i < nImages+1; i++) {
		selectImage(i);
		window_name = getTitle();
		window_names = Array.concat(window_names, window_name);
	}
	
	
	for (i = 0; i < window_names.length; i++) {	
		print(window_names[i]);
		selectWindow(window_names[i]);
		channel = substring(window_names[i], 0, 2);
		print("Chan: "+channel);
		if (channel == "C1") {
			close();
		}
		if (channel == "C2") {
			fluor_image = getTitle();
		}
		if (channel == "C3") {
			close();
		}
		if (channel == "C4") {
			close();
		}
	}

	
	selectWindow(fluor_image);
	run("Z Project...", "projection=[Max Intensity]");
	max_image = getTitle();
	saveAs("Tiff", dir_out+max_image);
	
	setMinAndMax(105, 300);
	run("Apply LUT");
	saveAs("Tiff", dir_view+"VIEW_ONLY_"+max_image);
		
	close("*");
}

processBioFormatFiles(dir_in);