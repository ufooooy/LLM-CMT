import express from 'express';
import fileUpload from 'express-fileupload';
import path from 'path';
import fs from 'fs';
import { asBlob } from 'html-docx-js-typescript';
import { fileURLToPath } from 'url';
import { exec } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const app = express(); // Initialize the Express application
app.use(express.json()); // Add this line to parse JSON bodies

// Add response for GET requests at '/'
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'demo.html'));
});

// Middleware to ensure 'upload' directory exists
app.use(async (req, res, next) => {
    const uploadDirectory = path.join(__dirname, 'upload');
    try {
        await fs.promises.access(uploadDirectory);
    } catch (err) {
        if (err.code === 'ENOENT') {
            // If directory does not exist, create it
            await fs.promises.mkdir(uploadDirectory);
        } else {
            console.error(err);
            res.status(500).send('Error checking upload directory.');
            return;
        }
    }
    next();
});

// Enable file upload
app.use(fileUpload({
    createParentPath: true,
    limits: { fileSize: 50 * 1024 * 1024 }, // 50 MB limit
    abortOnLimit: true
}));

// Handle POST request to save uploaded file under a new name based on timestamp
app.post('/upload', async (req, res) => {
    if (!req.files || Object.keys(req.files).length === 0) {
        console.log('No files uploaded'); // Debugging statement
        return res.status(400).send('No files were uploaded.');
    }

    let txtFile = req.files.fileUpload;

    // Ensure the file is a TXT file
    if (txtFile.mimetype !== 'text/plain') {
        return res.status(400).send('Unsupported file type.');
    }

    // Rename file with current timestamp
    const timestamp = Date.now();
    const newFileName = `${timestamp}.txt`;
    const destination = path.join(__dirname, 'upload', newFileName);

    // Move the file to the destination
    try {
        await txtFile.mv(destination);

        // Delete all other .txt files in the upload directory
        const files = await fs.promises.readdir(path.join(__dirname, 'upload'));
        const txtFiles = files.filter(file => file.endsWith('.txt') && file !== newFileName);
        for (const file of txtFiles) {
            await fs.promises.unlink(path.join(__dirname, 'upload', file));
        }

        res.send(`File uploaded with new filename: ${newFileName}`);
    } catch (err) {
        console.error(err);
        res.status(500).send(err.message);
    }
});

// Implement POST method to upload file and rename as 'm_'+current timestamp
app.post('/upload2', async (req, res) => {
    if (!req.files || Object.keys(req.files).length === 0) {
        console.log('No misuse files uploaded.');
        return res.status(400).send('No misuse files were uploaded.');
    }

    let jsonMisuseFile = req.files.misuseFileUpload;

    if (jsonMisuseFile.mimetype !== 'application/json') {
        return res.status(400).send('Unsupported misuse file type.');
    }

    const misuseTimestamp = Date.now();
    const misuseNewFileName = `m_${misuseTimestamp}.json`;
    const misuseDestination = path.join(__dirname, 'upload', misuseNewFileName);

    try {
        await jsonMisuseFile.mv(misuseDestination);

        const files = await fs.promises.readdir(path.join(__dirname, 'upload'));
        const jsonFiles = files.filter(file => file.startsWith('m_') && file.endsWith('.json') && file !== misuseNewFileName);
        for (const file of jsonFiles) {
            await fs.promises.unlink(path.join(__dirname, 'upload', file));
        }

        res.send(`Misuse file uploaded with new filename: ${misuseNewFileName}`);
    } catch (error) {
        console.error(error);
        res.status(500).send(error.message);
    }
});

app.get('/display', async (req, res) => {
    const uploadDirectory = path.join(__dirname, 'upload');
    let misuses = []; // Declare and initialize misuses

    try {
        // Get the list of files in the upload directory
        const files = await fs.promises.readdir(uploadDirectory);
        const misuseFiles = files.filter(file => file.startsWith('m_') && file.endsWith('.json')).sort((a, b) => b.split('.')[0] - a.split('.')[0]);
        
        if (misuseFiles.length !== 0) { // Corrected condition to check misuseFiles
            const misuseFile = path.join(uploadDirectory, misuseFiles[0]);
            const misuseData = await fs.promises.readFile(misuseFile, 'utf8');
            misuses = JSON.parse(misuseData);
        }

        // Call the Python script to transform the taxonomy
        const pythonScript = path.join(__dirname, 'model.py');

        exec(`python ${pythonScript}`, async (error, stdout, stderr) => {
            if (error) {
                console.error(`exec error: ${error}`);
                return res.status(500).send('Failed to transform taxonomy.');
            }

            // Use the script's output as the transformed file path
            const transformedFilePath = stdout.trim();
            // console.log(stdout.trim());

            const oTaxonomyData = await fs.promises.readFile(transformedFilePath, 'utf8');
            const oTaxonomy = JSON.parse(oTaxonomyData);

            // Function to transform the node structure
            function transformNode(node, misuses) {
                let resultNode = {
                    text: node.title,
                    id: node.title,
                    level: node.level
                };
                if (node.children) {
                    resultNode.children = node.children.map(child => transformNode(child, misuses));
                } else {
                    // 如果没有孩子节点则为叶子节点 <=> node.level === -1
                    resultNode.type = 'leaf';
                    // 遍历misuses将misuses中元素title等于node.title的explanation追加到resultNode.explanations
                    if (misuses && misuses.length) {
                        // 查找misuse数组，如果某个misuse的title等于当前节点的title，则将该misuse的explanation加入到explanations数组中。
                        resultNode.explanations = misuses.filter(misuse => misuse.title === node.title).map(x => x.explanation);
                    } else {
                        resultNode.explanations = [];
                    }
                }
                return resultNode;
            }

            // Transform the node structure
            const taxonomy = transformNode(oTaxonomy, misuses);

            // Convert the transformed structure to a string
            const taxonomyData = JSON.stringify(taxonomy, null, 4);
            // console.log(taxonomyData);

            res.send(taxonomyData);
        });
    } catch (err) {
        console.error(err);
        res.status(500).send('Failed to display file.');
    }
});

app.use('/export', express.static(path.join(__dirname, 'export')));

app.post('/export', async (req, res) => {
    try {
        const timestamp = Date.now(); // Get current timestamp
        const filename = `${timestamp}.doc`; // Construct filename with current timestamp
        const exportPath = path.join(__dirname, 'export', filename); // Directory to save the file

        // Make sure htmlContent is provided
        if (!req.body.htmlContent) {
            return res.status(400).send('No HTML content provided.');
        }

        // Convert HTML to DOCX format
        const converted = await asBlob(req.body.htmlContent); // Await the promise

        // Create and write data to the Word file
        await fs.promises.writeFile(exportPath, converted);

        // Delete all other .doc or .docx files in the export directory
        const files = await fs.promises.readdir(path.join(__dirname, 'export'));
        const docFiles = files.filter(file => file.endsWith('.doc')  && file !== filename);
        for (const file of docFiles) {
            // console.log(file);
            await fs.promises.unlink(path.join(__dirname, 'export', file));
        }

        // Generate download url
        const downloadUrl = `${req.protocol}://${req.get('host')}/export/${filename}`;

        // Send download url to the client
        res.send({ downloadUrl: downloadUrl });
    } catch (error) {
        console.error('Failed to create file:', error);
        res.status(500).send('Failed to export file.');
    }
});

// Function to delete files with specific extensions
function deleteFiles(directory, extensions) {
    fs.readdir(directory, (err, files) => {
        if (err) {
            console.error(`Error reading directory ${directory}:`, err);
            return;
        }
        files.forEach(file => {
            if (extensions.some(ext => file.endsWith(ext))) {
                fs.unlink(path.join(directory, file), err => {
                    if (err) {
                        console.error(`Error deleting file ${file}:`, err);
                    } else {
                        console.log(`Deleted file: ${file}`);
                    }
                });
            }
        });
    });
}


// Cleanup函数
function cleanup() {
    console.log('Cleanup...');
    const uploadDirectory = path.join(__dirname, 'upload');
    const exportDirectory = path.join(__dirname, 'export');
    const extensionsToDelete = ['.txt', '.json', '.docx', '.doc'];

    deleteFiles(uploadDirectory, extensionsToDelete);
    deleteFiles(exportDirectory, extensionsToDelete);
}

const port = 8000;

// Server启动事件
app.listen(port, () => {
    console.log('Server is running on port', port);
    cleanup(); // 启动时运行cleanup
});

// Server关闭事件
process.on('exit', () => {
    cleanup(); // 关闭时运行cleanup
});

process.on('SIGINT', () => {
    cleanup(); // Ctrl+C关闭时运行cleanup
    process.exit(0);
});

process.on('SIGTERM', () => {
    cleanup(); // kill命令关闭时运行cleanup
    process.exit(0);
});