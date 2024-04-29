//Settings to use in halo link:
//zoom = 10, transparency: off, ICC: o(n, label: off, scalebar: off
//if using 10x zoom export medium quality
// if using 5x soom use very high (sometimes halo link will bug, check it is actually HQ)

////defining functions to be used
function filter_by_color_to_ROIs(R_min, R_max, B_min, B_max, G_min, G_max) { 
	AI_first_title = getTitle();
	run("Split Channels");
	red_title = AI_first_title + " (red)";
	blue_title = AI_first_title + " (blue)";
	green_title = AI_first_title + " (green)";

	selectWindow(red_title);
	setThreshold(R_min, R_max);
	run("Convert to Mask");
	
	selectWindow(green_title);
	setThreshold(G_min, G_max);
	run("Convert to Mask");
	
	selectWindow(blue_title);
	setThreshold(B_min, B_max);
	run("Convert to Mask");
	
	run("Images to Stack", "use");
	stack_title = getTitle();
	run("Z Project...", "projection=[Min Intensity]");
	run("Dilate");
	AI_mask = getTitle();
	run("Analyze Particles...", "clear add");
	close(stack_title);
}

function label_cells_by_HALO_classification(AI_label) { 
	//AI_label should be either "pos" (positive) or "neg" (negative)
	// label_color_code should be = to the color HALO link displays as the label
	
	if (AI_label == "pos") { //RGB bounds for positive image label
		R_min = 220; R_max = 255; B_min = 0; B_max = 70; G_min = 0; G_max = 70;
	}
	if (AI_label == "neg") { //RBG bounds for negative image label
		R_min = 0; R_max = 80; B_min = 0; B_max = 100; G_min = 190; G_max = 255;
	}
	
	//open AI labeled image, and turn pixels matching the color code into ROIs
	open(AI_labeled_path);
	AI=getTitle();
	filter_by_color_to_ROIs(R_min, R_max, B_min, B_max, G_min, G_max);
	
	//open unlabeled image
	open(Un_image_path);
	raw_image = getTitle();
	run("Tile");
	selectWindow(raw_image);
	wait(500);//giving the image some time to open, otherwise it will ocassionally be duplicated?
	// loop through all ROIs, save them to a folder to be sorted
	ROI_count = roiManager("count");
	STOP_early = 0;
	if (ROI_count>0) {
		for (i = 0; i < ROI_count; i++) {
			roiManager("Select", i);
			roiManager("draw");
			roiManager("Select", i);
		    run("Enlarge...", "enlarge="+ROI_enlarge);
			run("Duplicate...", "title="+i+"marked_"+AI_label+"UWA_"+UWA_number+"Layer_"+Layer_number+"FOV_"+FOV_number);
			
			cell_title = getTitle();
			saveAs("png", folder_to_sort+cell_title);
			close();
			selectWindow(raw_image);
		
			STOP_early += 1;
			if (STOP_early==samples_per_fov_limit) {
				i=ROI_count;
			}
		}
		roiManager("Delete");
	}
	else {
		print("No " +AI_label+ " ROIs detected for image:" + AI_labeled_path);
	}

	close("*");
	roiManager("reset");	
}
///////////////////////end of functions being defined////////////////

//settings changed rarely:

download_path = ".../Downloads/" //path to where the downloaded HALO link captures are
folder_to_sort = ".../QC_folder/1_sort/" //path to the folder you want images saved to
check_for_negatives = true; //set to false if you only want this to capture the cells HALO marked as +
samples_per_fov_limit = 30; //set this to the max number of cells you want to analyze per image
ROI_enlarge = 35; //this determines how much space is left around the cell 


//Paste the base_file_name here:
pasted_file_name = "1234-A1-AT.svs(10X)_snapshot.png";
//enter 'snapshot numbers' for the AI labeled image (e.g.g 1234-A1-AT.svs(10X)_snapshot(1).png -> (1))
AI_image_snapshot_numbers = newArray(
	"", 	//1
	"(2)",	//2
	"(4)",	//3
	"(6)",	//4
	"(8)",	//5
	"(10)",	//6
	"(12)",	//7
	"(14)",	//8
	"(16)",	//9
	"(18)"	//10
);
//enter 'snapshot numbers' for the unlabeled images corresponding to the above images
UN_image_snapshot_numbers = newArray(
	"(1)",	//1
	"(3)",	//2
	"(5)",	//3
	"(7)",	//4
	"(9)",	//5
	"(11)", //6
	"(13)",	//7
	"(15)",	//8
	"(17)",	//9
	"(19)"	//10
);
//enter layer/FOV numbers for the above images
layer_numbers = newArray(5, 5, 5, 5, 5, 3, 3, 3, 3, 3);
FOV_numbers = newArray(1, 2, 3, 4, 5, 1, 2, 3, 4, 5);

for (j = 0; j < AI_image_snapshot_numbers.length; j++) {	
	png_index = indexOf(pasted_file_name, ".png");
	base_file_name = substring(pasted_file_name, 0, png_index);
	
	//pull out info specific to each pair of images
	AI_image_name = base_file_name+AI_image_snapshot_numbers[j]+".png";
	unlabeled_image_name = base_file_name+UN_image_snapshot_numbers[j]+".png";
	Layer_number = layer_numbers[j];
	FOV_number = FOV_numbers[j];
	UWA_number = substring(AI_image_name, 0,4); //pull the first 4 characters from the file name (assume those are the UWA)
	//path to open the image pair
	AI_labeled_path = download_path+AI_image_name;
	Un_image_path = download_path+unlabeled_image_name;
	
	//calling functions opens images and saves cells with file name corresponding to HALO classification, UWA#, Layer#, and FOV#
	setForegroundColor(0, 0, 0);
	label_cells_by_HALO_classification("pos");
	
	if (check_for_negatives==true) {
		label_cells_by_HALO_classification("neg");
	}
}












