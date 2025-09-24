function [ r ] = MATLABStandalone_NSC_ray_trace( args )
 
if ~exist('args', 'var')
    args = [];
end
 
TheApplication = InitConnection();
if isempty(TheApplication)
   
    r = [];
else
    try
        r = BeginApplication(TheApplication, args);
        CleanupConnection(TheApplication);
    catch err
        CleanupConnection(TheApplication);
        rethrow(err);
    end
end
end

function[r] = BeginApplication(TheApplication, args)
    import ZOSAPI.*;
    apiPath = System.String.Concat(TheApplication.SamplesDir,'\API\Matlab'); 
    if (exist(char(apiPath)) == 0) mkdir(char(apiPath)); end;

    TheSystem = TheApplication.PrimarySystem; 
    sampleDir = TheApplication.SamplesDir;

    csvIn = "C:\Users\ELIZA\Downloads\satellite_state_log (3).csv";
    testFile = "C:\Users\ELIZA\OneDrive - The University of Chicago\Zemax files\GSOPTICS_SM10_12.ZOS"; 
    TheSystem.LoadFile(testFile, false);
    
    csvOut = 'C:\Users\ELIZA\OneDrive - The University of Chicago\MATLAB\ZOS_API projects';
    if ~exist(csvOut,'dir'), mkdir(csvOut); end
    outFile = fullfile(csvOut, sprintf('nsc_centroids_%s.csv', datestr(now,'yyyymmdd_HHMM')));

    ogsLatDeg = 41.789722;
    ogsLonDeg = -87.599724;

    TheNCE = TheSystem.NCE;
    det = [4,5,14];
    Ndet = numel(det);
    obj = TheNCE.GetObjectAt(1);

    C = readtable(csvIn);
    AB = calculate_42_angles(csvIn, ogsLatDeg, ogsLonDeg);
    K = height(AB);

    tiltX_deg = asind( sind(AB.alpha_deg) .* sind(AB.beta_deg) );
    tiltY_deg = atan2d( sind(AB.alpha_deg).*cosd(AB.beta_deg), cosd(AB.alpha_deg) );

    xC = nan(K,Ndet);
    yC = nan(K,Ndet);
    power = nan(K,Ndet);
    radii = nan(K,Ndet);
    NSCRayTrace = TheSystem.Tools.OpenNSCRayTrace();
    NSCRayTrace.SplitNSCRays = true;
    NSCRayTrace.ScatterNSCRays = false;
    NSCRayTrace.UsePolarization = true;
    NSCRayTrace.IgnoreErrors = true;
    NSCRayTrace.SaveRays = false;

    for k = 1:50
        obj.TiltAboutX = tiltX_deg(k);
        obj.TiltAboutY= tiltY_deg(k);
        NSCRayTrace.ClearDetectors(true);
        NSCRayTrace.RunAndWaitForCompletion();
        
        for i = 1:Ndet
            detIndex = det(i);
            chosenDS = NaN;
            [~, rows, cols] = TheNCE.GetDetectorDimensions(detIndex);
            for ds = [1 0]
                buf = NET.createArray('System.Double', TheNCE.GetDetectorSize(detIndex));
                TheNCE.GetAllDetectorData(detIndex, ds, TheNCE.GetDetectorSize(detIndex), buf);
                Itry = reshape(buf.double, rows, cols); 
                if any(Itry(:))
                    chosenDS = ds;
                    break
                end
            end
    
            if isnan(chosenDS) 
                xC(k,i)=NaN; yC(k,i)=NaN; power(k,i)=NaN; radii(k,i)=NaN;
                continue
            end
            
            [okP, P_api] = TheNCE.GetDetectorData(detIndex, chosenDS, 0);
            [okX, x_api] = TheNCE.GetDetectorData(detIndex, chosenDS, 4);
            [okY, y_api] = TheNCE.GetDetectorData(detIndex, chosenDS, 5);
    
            if okP, power(k,i) = P_api; else, power(k,i) = NaN; end
    
            if okX && okY && (x_api ~= 0 || y_api ~= 0)
                xC(k,i) = x_api;
                yC(k,i) = y_api;
            else
                I = reshape(buf.double, rows, cols);     
                I(I < 0) = 0;
                x = linspace(-1, 1, cols);  
                y = linspace(-1, 1, rows);
                [Xg, Yg] = meshgrid(x, y);
                S = sum(I(:));
                if S > 0
                    xC(k,i) = sum(sum(I .* Xg)) / S;
                    yC(k,i) = sum(sum(I .* Yg)) / S;
                else
                    xC(k,i) = NaN; yC(k,i) = NaN;
                end
            end
    
            if ~isnan(xC(k,i)) && ~isnan(yC(k,i))
                radii(k,i) = hypot(xC(k,i), yC(k,i));
            else
                radii(k,i) = NaN;
            end
        end
    end

    NSCRayTrace.Close();

    T = table(string(C.timestamp), tiltX_deg(:), tiltY_deg(:), AB.alpha_deg(:), AB.beta_deg(:), 'VariableNames', {'timestamp','tilt X', 'tilt Y', 'alpha', 'beta'});

    for i = 1:Ndet
        did = det(i);
        T.(sprintf('xC_det%d', did))     = xC(:,i);
        T.(sprintf('yC_det%d', did))     = yC(:,i);
        T.(sprintf('Centroid_det%d', did)) = radii(:,i);
    end

    writetable(T, outFile);
    fprintf('Wrote combined CSV: %s\n', outFile);

    r = [];
end

function app = InitConnection()
import System.Reflection.*;
zemaxData = winqueryreg('HKEY_CURRENT_USER', 'Software\Zemax', 'ZemaxRoot');
NetHelper = strcat(zemaxData, '\ZOS-API\Libraries\ZOSAPI_NetHelper.dll');
NET.addAssembly(NetHelper);
success = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize();
if success == 1
    LogMessage(strcat('Found OpticStudio at: ', char(ZOSAPI_NetHelper.ZOSAPI_Initializer.GetZemaxDirectory())));
else
    app = [];
    return;
end
NET.addAssembly(AssemblyName('ZOSAPI_Interfaces'));
NET.addAssembly(AssemblyName('ZOSAPI'));
TheConnection = ZOSAPI.ZOSAPI_Connection();
app = TheConnection.CreateNewApplication();
if isempty(app)
   HandleError('An unknown connection error occurred!');
end
if ~app.IsValidLicenseForAPI
    HandleError('License check failed!');
    app = [];
end
end

function LogMessage(msg)
disp(msg);
end
 
function HandleError(error)
ME = MXException(error);
throw(ME);
end
 
function  CleanupConnection(TheApplication)
TheApplication.CloseApplication();
end
