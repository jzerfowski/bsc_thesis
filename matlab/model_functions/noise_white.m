function [Ie_noise, Ii_noise] = noise_white(reg, tnumb, noiseseed, noisecor, Ienoise, Iinoise)
%BROWNIAN_NOISE Summary of this function goes here
%   Detailed explanation goes here

s = RandStream('mcg16807','Seed', noiseseed);
RandStream.setGlobalStream(s);

nsigw = randn(reg,tnumb);
nsigw(reg,:) = noisecor*nsigw(1,:) + (1-noisecor)*nsigw(reg,:);
Ii_noise = single(bsxfun(@times,Iinoise(1:reg)',nsigw));
Ie_noise = single(bsxfun(@times,Ienoise(1:reg)',nsigw));
clear nsigw

end

